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
import hashlib
import shutil
import unittest
from unittest.mock import MagicMock
from config import CFG
import utils
import mess_processor
from models import Event
from wand.image import Image


json_str = {
  "bucket": "eulixspace-files",
  "contentType": "image/jpeg",
  "eventName": "put",
  "key": "",
  "name": "",
  "size": 5000,
  "betagPath": "",
  "diskPath": ""
}


result_dir = os.path.join(CFG.ROOT_DATA_DIR, CFG.BUCKET_TARGET)


def file_md5(filename):
    md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()


def mock_put_jpg_event(filename):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    image_path = os.path.join(current_dir, filename)
    mock_event = Event(message=dict(json_str))
    mock_event.get_file_path = MagicMock(return_value=image_path)
    mock_event.content_type = "image/jpeg"
    mock_event.event_name = "put"
    mock_event.object_key = file_md5(image_path)
    mock_event.object_size = os.path.getsize(image_path)
    return mock_event


def mock_put_mp4_event():
    image_name = "the_jpg.jpg"
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_dir, image_name)
    mock_event = Event(message=dict(json_str))
    mock_event.get_file_path = MagicMock(return_value=file_path)
    mock_event.content_type = "image/jpeg"
    mock_event.event_name = "put"
    return mock_event


# def mock_put_doc_event():
#     filename = "the_docx.docx"
#     current_dir = os.path.abspath(os.path.dirname(__file__))
#     file_path = os.path.join(current_dir, filename)
#     mock_event = Event(message=dict(json_str))
#     mock_event.get_file_path = MagicMock(return_value=file_path)
#     mock_event.content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#     mock_event.event_name = "put"
#     mock_event.object_key = file_md5(file_path)
#     return mock_event


class TestMessProcessor(unittest.TestCase):
    def setUp(self) -> None:
        for name in os.listdir(result_dir):
            file_path = os.path.join(result_dir, name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                if str(file_path).endswith(".run"):
                    continue
                shutil.rmtree(file_path)

    def test_process_event(self):
        event = mock_put_jpg_event("the_jpg.jpg")
        mess_processor.process_event(event)

    # def test_process_event_with_docx(self):
    #     event = mock_put_doc_event()
    #     mess_processor.process_event(event)

    # def test_generate_doc_to_pdf(self):
    #     event = mock_put_doc_event()
    #     mess_processor.generate_pdf_preview(event)
    #     t_path = utils.gen_preview_pdf_path(event.object_key)
    #     self.assertTrue(os.path.exists(t_path))
    #     self.assertTrue(os.path.getsize(t_path) > 0)

    def test_jpeg_to_thumbnail(self):
        event = mock_put_jpg_event("the_jpg.jpg")
        mess_processor.generate_thumbnail(event)
        t_path = utils.gen_thumb_path(event.disk_path, event.object_key)
        self.assertTrue(os.path.exists(t_path))
        self.assertTrue(os.path.getsize(t_path) > 0)

    def test_jpeg_to_preview(self):
        event = mock_put_jpg_event("shutu.jpg")
        mess_processor.generate_image_preview(event, CFG.PREVIEW_MIN_SIZE)
        expected_path = utils.gen_preview_img_path(event.disk_path, event.object_key)
        self.assertTrue(os.path.exists(expected_path))
        self.assertTrue(os.path.getsize(expected_path) > 0)

        raw_ratio = compute_image_ratio(event.get_file_path())
        ratio = compute_image_ratio(expected_path)
        self.assertAlmostEqual(raw_ratio, ratio)


def compute_image_ratio(filename):
    with Image(filename=filename) as img:
        img.auto_orient()
        size = utils.ImgDims(width=img.width, height=img.height)
        return size.ratio()


if __name__ == "__main__":
    unittest.main()
