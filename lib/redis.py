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

import time

from walrus import *
import logging
from config import CFG
from mess_processor import process_message


logger = logging.getLogger("preview")


class RedisHelper:

    def __init__(self, cfg: CFG):
        self.cfg = cfg
        self.host = self.cfg.REDIS_HOST
        self.port = self.cfg.REDIS_PORT
        self.db = self.cfg.REDIS_DB
        self.password = self.cfg.REDIS_PASSWORD
        self.__conn = Walrus(host=self.host, port=self.port, password=self.password, db=0)
        self.chan_sub = self.cfg.REDIS_CHANNEL_NAME

        # self.group_name = "preview"

    # def subscribe(self):
    #     # 返回发布订阅对象，通过这个对象你能1）订阅频道 2）监听频道中的消息
    #     pub = self.__conn.pubsub()
    #     # 订阅频道，与publish()中指定的频道一样。消息会发布到这个频道中
    #     pub.subscribe(self.chan_sub)
    #     # pub.listen()
    #     for item in pub.listen():
    #         if item['type'] == 'message':
    #             process_message(item['data'])
    #     # ret = pub.parse_response()  # [b'subscribe', b'fm86', 1]
    #     # print("ret:%s" % ret)
    #     # return pub

    def read_msg(self):
        # self.__conn.xgroup_create(self.chan_sub, "preview", "$")
        # xids = []
        lastid = "0-0"
        check_backlog = True

        stream = self.__conn.Stream(self.chan_sub)

        # messages = list(stream)

        while True:
            # if check_backlog:
            #     consumer_id = lastid
            # else:
            #     consumer_id = '$'
            msg = stream.read(block=0, last_id=lastid)
            # print(lastid)
            # if not msg:  # 如果 block 不是 0或者为空, 会需要这段
            #     logger.info("Timeout!")
            #     time.sleep(3)  # 空值等待 3s
            #     continue
            # elif len(msg[0][1]) == 0:
            #     check_backlog = False

            str_msg = {key.decode(): val.decode() for key, val in msg[0][1].items()}
            if str_msg:
                try:
                    process_message(str_msg)
                except Exception as e:
                    logger.exception(e)
                finally:
                    lastid = msg[0][0]
            stream.delete(msg[0][0].decode())
        # msg = self.__conn.({self.chan_sub: '$'}, None, 0)
        # xid = msg[0][1][0][0]
        # print(xid)
        # self.__conn.xack(self.chan_sub, self.group_name, xid)
        # try:
        #     logger.info(f"get message : {msg} ")
        #     process_message(msg[0][1][0][1])
        # except Exception as e:
        #     logger.exception(e)
        # self.del_msg(xid)

    # def del_msg(self, xid):
    #     self.__conn.delete()
