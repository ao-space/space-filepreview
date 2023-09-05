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

"""读取消息，生成缩略图"""
import logging

from config import CFG
# from lib.mq import ReliableConsumer
from lib.redis import RedisHelper

logger = logging.getLogger('preview')

if __name__ == '__main__':
    logger.info("Connecting to redis...")
    consumer = RedisHelper(CFG)
    logger.info("Start consuming...")
    # consumer.start_consuming(mess_processor.process_message)
    # consumer.subscribe()
    consumer.read_msg()
