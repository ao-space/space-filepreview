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
import tempfile
import atexit
import logging

logger = logging.getLogger("preview")

logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='[%(levelname).3s] %(asctime)s: %(message)s', datefmt='%m-%d %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)

pg_logger = logging.getLogger("PreviewGenerator")
pg_logger.addHandler(logging.NullHandler())


def get_env_int(key, default):
    try:
        return int(os.getenv(key, default))
    except ValueError as e:
        logger.warning("env %s must be a int: %s", key, e)
        return default


class Config:
    REDIS_HOST = "eulixspace-redis"
    REDIS_PORT = 6379
    REDIS_DB = 0
    # MQ_USERNAME = "root"
    REDIS_PASSWORD = "mysecretpassword"
    # MQ_ROUTING = "fileChangelogs"
    # MQ_EXCHANGE = "fileChangelogs"
    # MQ_EXCHANGE_KIND = "direct"
    REDIS_CHANNEL_NAME = "fileChangelogs"
    BUCKET_SOURCE = "eulixspace-files"
    BUCKET_TARGET = "eulixspace-files-processed"
    TMP_PROCESSED_DIR_WIN = "/tmp"  # 处理缩略图时，会使用一个临时目录来处理，如果处理的文件较大，则需要该目录有相应的可用空间
    PREVIEW_MIN_SIZE = 1  # 如果图片小于该大小则不生成预览图（单位：字节）
    PREVIEW_MAX_SIZE = 0  # 如果文件大于该大小则不生成预览图（单位：字节） 如果设为 0 即忽略该参数（可以无限大）
    DEBUG_MODE = 0  # 是否开启 debug 日志级别 （0 表示不开启，其他表示开启，默认不开启）
    ROOT_DATA_DIR = "/data/"

    def __init__(self):
        self._load_env_config()

    def _load_env_config(self):
        self.REDIS_HOST = os.getenv("REDIS_HOST", self.REDIS_HOST)
        self.REDIS_PORT = os.getenv("REDIS_PORT", self.REDIS_PORT)
        self.REDIS_DB = os.getenv("REDIS_PORT", self.REDIS_DB)
        # self.MQ_USERNAME = os.getenv("MQ_USERNAME", self.MQ_USERNAME)
        self.REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", self.REDIS_PASSWORD)
        # self.MQ_ROUTING = os.getenv("MQ_ROUTING", self.MQ_ROUTING)
        # self.MQ_EXCHANGE = os.getenv("MQ_EXCHANGE", self.MQ_EXCHANGE)
        # self.MQ_EXCHANGE_KIND = os.getenv("MQ_EXCHANGE_KIND", self.MQ_EXCHANGE_KIND)
        self.REDIS_CHANNEL_NAME = os.getenv("REDIS_CHANNEL_NAME", self.REDIS_CHANNEL_NAME)
        self.BUCKET_SOURCE = os.getenv("BUCKET_SOURCE", self.BUCKET_SOURCE)
        self.BUCKET_TARGET = os.getenv("BUCKET_TARGET", self.BUCKET_TARGET)
        self.PREVIEW_MIN_SIZE = get_env_int("PREVIEW_MIN_SIZE", self.PREVIEW_MIN_SIZE)
        self.PREVIEW_MAX_SIZE = get_env_int("PREVIEW_MAX_SIZE", self.PREVIEW_MAX_SIZE)
        self.DEBUG_MODE = get_env_int("DEBUG_MODE", self.DEBUG_MODE)
        self.ROOT_DATA_DIR = os.getenv("ROOT_DATA_DIR", self.ROOT_DATA_DIR)


class TmpDir:

    def __init__(self, father_dir: str):
        self.father_dir = father_dir
        self._source_dir = None
        self._cache_dir = None

    @staticmethod
    def remove_temp_dir(tmp_dir):
        try:
            tmp_dir.cleanup()
            logger.debug("Temporary directory %s has been cleanup", tmp_dir.name)
        except Exception:
            pass

    @property
    def source_dir(self):
        if not self._source_dir:
            self._source_dir = tempfile.TemporaryDirectory(prefix="eulixspace-filepreview-source", dir=self.father_dir)
            logger.debug("Make a temporary directory %s for save source file", self._source_dir.name)
            atexit.register(self.remove_temp_dir, self._source_dir)
        return self._source_dir

    @property
    def cache_dir(self):
        if not self._cache_dir:
            self._cache_dir = tempfile.TemporaryDirectory(prefix="eulixspace-filepreview-cache", dir=self.father_dir)
            logger.debug("Make a temporary directory %s for cache result", self._cache_dir.name)
            atexit.register(self.remove_temp_dir, self._cache_dir)
        return self._cache_dir


CFG = Config()
if not CFG.DEBUG_MODE:
    logger.setLevel(logging.INFO)

PREVIEW_SUFFIX = "preview"
