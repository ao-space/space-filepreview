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

import os
from config import CFG, PREVIEW_SUFFIX
from preview_generator.manager import PreviewManager
from models import ThumbnailFormat


def create_preview_manager(result_dir: str = None):
    if not result_dir:
        result_dir = os.path.join(CFG.ROOT_DATA_DIR, CFG.BUCKET_TARGET, ".run")
    preview_manager = PreviewManager(result_dir, create_folder=True)
    return preview_manager


def gen_preview_img_path(disk_path, s_key):
    key_dir = gen_preview_dir(disk_path, s_key)
    filename = PREVIEW_SUFFIX + ".jpg"
    return os.path.join(key_dir, filename)


def gen_preview_pdf_path(disk_path, s_key):
    key_dir = gen_preview_dir(disk_path, s_key)
    filename = PREVIEW_SUFFIX + ".pdf"
    return os.path.join(key_dir, filename)


def gen_thumb_path(disk_path, s_key):
    key_dir = gen_preview_dir(disk_path, s_key)
    filename = ThumbnailFormat.filename
    return os.path.join(key_dir, filename)


def gen_preview_dir(disk_path, key):
    return os.path.join(disk_path, CFG.BUCKET_TARGET, key[:2], key[2:4], key)


def gen_src_path(key):
    return os.path.join(CFG.ROOT_DATA_DIR, CFG.BUCKET_SOURCE, key[:2], key[2:4], key)

class ImgDims(object):
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def ratio(self) -> float:
        return self.width / self.height

    def max_dim(self) -> int:
        return max(self.width, self.height)

    def __str__(self) -> str:
        return "{}x{}".format(self.width, self.height)
