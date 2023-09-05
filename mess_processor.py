# Copyright (c) 2022 Institute of Software, Chinese Academy of Sciences (ISCAS)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""缩略图转换业务"""
import logging
import signal
import os
import shutil
import time

from PIL import PngImagePlugin
from pika.amqp_object import Properties
from pika.channel import Channel

import models
import utils
# from lib.redis import RedisHelper
from models import Event, ThumbnailFormat
from config import CFG
from preview_generator.exception import PreviewGeneratorException
from exceptions import PreviewError

logger = logging.getLogger("preview")

LARGE_ENOUGH_NUMBER = 100
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024 ** 2)

IGNORED_CONTENT_TYPE = ["application/gzip", "application/x-rar-compressed", "application/zip"]
manager = utils.create_preview_manager()
target_bucket = CFG.BUCKET_TARGET


class ExitHandler:
    def __init__(self, ch: Channel, method):
        self.ch = ch
        self.method = method

    def __call__(self, signals, frame_type):
        logger.warning("received a SIGTERM signal, try reject message and will exit...")
        reject_message_quietly(self.ch, self.method)


def reject_message_quietly(ch: Channel, method):
    """拒收消息， 不抛出异常"""
    try:
        ch.basic_reject(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.warning("Failed to reject message: %s", e)


# def ack_message(ch, method, event_id=None):
#     try:
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#     except Exception as e:
#         warn = f"Failed to acknowledge message: {e}"
#         if event_id:
#             warn = warn + f", event_id: {event_id}"
#         logger.warning(warn)


def process_message(body):
    """需要手动确认消息"""
    try:
        event = Event(body)  # json 体内容可以参看 docs/mess_demo.json

        process_event(event)
        logger.info(f"[Done] event {event.event_id}")
        time.sleep(0.2)
        # signal.signal(signal.SIGTERM, ExitHandler(ch, method))

        # ack_message(ch, method, event.event_id)

    except PreviewError as e:
        logger.error(e)
        # ack_message(ch, method)
    except KeyboardInterrupt as e:
        logger.exception("User cancelled: %s", e)
        # reject_message_quietly(ch, method)

    except Exception as e:
        logger.exception(e)
        # ack_message(ch, method)


def process_event(event: Event):
    logger.info(f"[Received] event {event.event_id}")
    if event.event_name == "delete":
        delete_event_object(event)
    elif event.event_name.startswith("put"):
        handle_event_create(event,
                            CFG.PREVIEW_MAX_SIZE,
                            CFG.PREVIEW_MIN_SIZE)
    else:
        # ignored
        logger.debug("[Ignored] message %s", event.event_id)


def delete_event_object(event) :
    """删除事件中 object 的缩略图，预览图等相关的资源"""
    preview_dir = utils.gen_preview_dir(event.object_key)
    src_path = utils.gen_src_path(event.object_key)
    try:
        exist = os.path.isfile(src_path)
        if not exist:
            if shutil.rmtree(preview_dir):
                logger.info("Successfully delete %v", preview_dir)

    except Exception as e:
        logger.warning("Failed to delete preview %s: %s", preview_dir, e)


def check_thumbnail_exists(event) -> bool:
    t_key = utils.gen_thumb_path(event.disk_path, event.object_key)
    exist = os.path.isfile(t_key)
    if not exist:
        return False
    else:
        return bool(os.path.getsize(t_key))


def handle_event_create(event, max_size, min_size):
    """
    max_size：大于该大小，不处理， 等于 0 忽略该参数
    min_size：小于该大小，不处理
    """
    if event.object_size == 0:
        logger.info(f"[Ignored] The object {event.object_key} size is zero")
    elif event.object_size and max_size != 0 and event.object_size > max_size:
        logger.info(f"[Ignored] The object {event.object_key} size is larger than {max_size}")
    else:
        exist = check_thumbnail_exists(event)
        if exist:
            logger.info("[Ignored] thumbnail image %s had exist", event.object_key)
        else:
            try:
                source_obj_to_target_image(event, min_size)
            except PreviewGeneratorException as e:
                logger.warning("Failed to generate image for %s: %s", event.event_id, e)


def source_obj_to_target_image(event, min_size):
    """
    接受一个事件，读取原图片，然后生成图片，保存
    """
    supported_mimetypes = manager.get_supported_mimetypes()
    supported_mimetypes.append("application/octet-stream")

    supported = check_type_supported(event, supported_mimetypes)
    if not supported:
        logger.debug("Ignored generate thumbnails for %s , content-type: %s", event.object_key,
                     event.content_type)
        return

    # 缩略图
    logger.debug("Start to generate thumbnails for %s, content-type: %s",
                 event.object_key,
                 event.content_type)
    generate_thumbnail(event)

    # 压缩图, 只生成图片的预览图
    logger.debug("Start to generate compressed image for %s, content-type: %s",
                 event.object_key,
                 event.content_type)
    if event.content_type.startswith("image/") or event.content_type.startswith("video/"):
        generate_image_preview(event, min_size)


def delete_file(path: str, delete_lock=False):
    """删除对应路径的文件"""
    try:
        os.remove(path)
        if delete_lock:
            dir_path = os.path.dirname(path)
            filename = os.path.basename(path)
            file_no_suf = os.path.splitext(filename)[0]
            if "-" in file_no_suf:
                lock_name = file_no_suf.split("-")[0] + ".lock"
            else:
                lock_name = file_no_suf + ".lock"
            lock_path = os.path.join(dir_path, lock_name)
            os.remove(lock_path)
    except Exception as e:
        logger.debug("Failed to remove temporary file %s: %s", path, e)


def check_type_supported(event, supported_mimetypes):
    if event.content_type in IGNORED_CONTENT_TYPE:
        return False
    else:
        return event.content_type in supported_mimetypes


def generate_thumbnail(event):
    tmp_path = manager.get_jpeg_preview(file_path=event.get_file_path(),
                                        width=ThumbnailFormat.width,
                                        height=ThumbnailFormat.height)
    target_path = utils.gen_thumb_path(event.disk_path, event.object_key)
    move_preview_file(tmp_path, target_path)
    logger.debug("Successfully upload thumbnails for %s", event.object_key)
    return target_path


def generate_image_preview(event, min_size):
    file_path = event.get_file_path()
    if event.object_size and int(event.object_size) < min_size:
        logger.debug("Ignored, the origin image less than %s", min_size)
        return
    if event.content_type.startswith("image/"):
        tmp_path = manager.get_jpeg_preview(file_path=file_path, height=768)
    else:
        tmp_path = manager.get_jpeg_preview(file_path=file_path)
    target_path = utils.gen_preview_img_path(event.disk_path, event.object_key)
    move_preview_file(tmp_path, target_path)
    logger.debug("Successfully save compressed image for %s", event.object_key)
    return target_path


def generate_pdf_preview(event: models.Event):
    tmp_path = manager.get_pdf_preview(event.get_file_path())
    target_path = utils.gen_preview_pdf_path(event.disk_path, event.object_key)
    move_preview_file(tmp_path, target_path)
    logger.debug("Successfully save pdf preview for %s", event.object_key)
    return target_path


def move_preview_file(src, dst, delete_lock=True):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    os.sync()
    delete_file(path=src, delete_lock=delete_lock)
