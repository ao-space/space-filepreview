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



class PreviewGeneratorException(Exception):
    pass


class IntermediateFileBuildingFailed(PreviewGeneratorException):
    """
    Exception raised when building of intermediate file failed.
    """

    pass


class PreviewAbortedMaxAttempsExceeded(PreviewGeneratorException):
    """
    Exception raised when max attemps of preview generation are exceeded.
    """

    pass


class UnavailablePreviewType(PreviewGeneratorException):
    """
    Exception raised when a preview method is not implemented for the type of
    file you are processing
    """

    pass


class UnsupportedMimeType(PreviewGeneratorException):
    """
    Exception raised when a file mimetype is not found in supported mimetypes
    """

    pass


class InputExtensionNotFound(PreviewGeneratorException):
    """
    Exception raised if input extension is not found from mimetype.
    """

    pass


class BuilderNotLoaded(PreviewGeneratorException):
    """
    Exception raised when the factory is used but no builder has been loaded
    You must call factory.load_builders() before to use the factory
    """

    pass


class BuilderDependencyNotFound(PreviewGeneratorException):
    pass
