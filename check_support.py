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

from preview_generator.manager import PreviewManager


def gen_tag(r):
    if r:
        return "√"
    else:
        return "x"


if __name__ == "__main__":
    pm = PreviewManager("/tmp")
    supported = pm.get_supported_mimetypes()
    print("[{}] support image".format(gen_tag("image/jpeg" in supported)))
    print("[{}] support ppt".format(gen_tag("application/vnd.ms-powerpoint" in supported)))
    print("[{}] support docx".format(gen_tag("application/wps-office.docx" in supported)))
    print("[{}] support video".format(gen_tag("video/mp4" in supported)))
