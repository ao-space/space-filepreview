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

# Produces a PDF for the SLA passed as a parameter.
# Uses the same file name and replaces the .sla extension with .pdf
#
# usage:
# scribus -g -py to-pdf.py -- file.sla
#
# license:
# (c) MIT Ale Rimoldi

import logging
import sys

import scribus

from preview_generator.utils import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
if scribus.haveDoc():
    pdf = scribus.PDFfile()
    pdf.file = sys.argv[1]
    pdf.save()
else:
    logger.error("No file open in scribus")
