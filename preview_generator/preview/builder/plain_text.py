# -*- coding: utf-8 -*-
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


import typing

from preview_generator.preview.builder.office__libreoffice import OfficePreviewBuilderLibreoffice


class PlainTextPreviewBuilder(OfficePreviewBuilderLibreoffice):
    weight = 50

    @classmethod
    def get_label(cls) -> str:
        return "Plain text files"

    @classmethod
    def get_supported_mimetypes(cls) -> typing.List[str]:
        return [
            "text/plain",
            "text/html",
            "text/xml",  # Info - B.L - Compatibility between debian and ubuntu
            "application/xml",
            "application/javascript",
        ]

    def build_text_preview(
        self,
        file_path: str,
        preview_name: str,
        cache_path: str,
        page_id: int = 0,
        extension: str = ".txt",
    ) -> None:
        """
        generate the text preview
        """
        with open(file_path, "rb") as txt:
            with open(
                "{path}{extension}".format(path=cache_path + preview_name, extension=extension),
                "wb",
            ) as output_text:
                buffer = txt.read(1024)
                while buffer:
                    output_text.write(buffer)
                    buffer = txt.read(1024)

    def has_text_preview(self) -> bool:
        return True
