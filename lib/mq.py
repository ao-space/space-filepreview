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

import pika
from config import CFG
from typing import Callable
import logging

logger = logging.getLogger("preview")


class ReliableConsumer:
    """可靠的日志消费模型, 需要手动确认消息"""

    def __init__(self, cfg: CFG):
        self.cfg = cfg
        self.host = self.cfg.MQ_HOST
        self.port = self.cfg.MQ_PORT
        self.username = self.cfg.MQ_USERNAME
        self.password = self.cfg.MQ_PASSWORD
        self._connection = None
        self._channel = None
        self.queue_name = self.cfg.MQ_QUEUE_NAME
        self.exchange_name = self.cfg.MQ_EXCHANGE
        self.exchange_type = self.cfg.MQ_EXCHANGE_KIND
        self.routing_key = self.cfg.MQ_ROUTING
        self.register_queue()
        self.set_qos()

    def register_queue(self):
        self.declare_exchange()
        self.declare_queue()
        self.queue_bind()

    @property
    def connection(self):
        if not self._connection:
            credentials = pika.PlainCredentials(self.username, self.password)
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    credentials=credentials,
                    heartbeat=15 * 60,
                ))
        return self._connection

    @property
    def channel(self):
        if not self._channel:
            self._channel = self.connection.channel()
        return self._channel

    def declare_exchange(self):
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=self.exchange_type,
            durable=True,
        )

    def declare_queue(self):
        self.channel.queue_declare(
            queue=self.queue_name,
            durable=True,
            arguments={"x-queue-mode": "lazy"}  # 惰性队列减少内存占用
        )

    def queue_bind(self):
        self.channel.queue_bind(
            queue=self.queue_name,
            exchange=self.exchange_name,
            routing_key=self.routing_key,
        )

    def set_qos(self):
        self.channel.basic_qos(prefetch_count=1)

    def start_consuming(self, callback: Callable):
        self.channel.basic_consume(
            on_message_callback=callback,
            queue=self.queue_name,
            auto_ack=False,
        )
        self.channel.start_consuming()
