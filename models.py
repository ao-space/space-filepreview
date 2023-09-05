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

import json

import config
from config import CFG
from exceptions import EncodeEventError


class Event:
    def __init__(self, message: dict):
        try:
            self.event = message
            self.event_name = self.event['eventName']
            self.object_key = self.event['key']
            self.bucket = self.event['bucket']
            self.content_type = self.event.get("contentType", "")
            self.name = self.event.get('name')
            self.object_size = self.event.get('size')
            self.event_id = self.event_name + ":" + self.object_key
            self.betag_path = self.event['betagPath']
            self.disk_path = self.event['diskPath']
        except KeyError as e:
            raise EncodeEventError(f"message lack {e}, raw message: {message}")

    def get_file_path(self, cfg: config.Config = CFG) -> str:
        # return cfg.ROOT_DATA_DIR + self.bucket + "/" + self.object_key[
        #                                                 0:2] + "/" + self.object_key[2:4] \
        #        + "/" + self.object_key
        return self.betag_path

class ThumbnailFormat:
    thumb_name = "thumbnail"
    width = 360
    height = 360
    extension = ".jpg"
    filename = thumb_name + extension
