#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : stream_controller.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 31.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

import redis
import time
from RealtimeDataMessage import *


class Stream_controller():
    def __init__(self, topic):
        self.stream = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.db = self.stream
        self.pubsub = self.stream.pubsub()
        self.topic = topic
        self.pubsub.subscribe(self.topic)
        self.msgParser = MessageParser()
        self.last_recv_data = []

    def listen(self):
        while True:
            msg = self.pubsub.get_message()
            if msg:
                rec = False
                try:
                    rec = msg.get('data').decode('utf-8')  # remove b' encoding
                    if self.msgParser.decode(rec, ret_type=RET_TYPE.LIST_KEY_VALUE) != False:
                        self.last_recv_data = self.msgParser.decode(
                            rec, ret_type=RET_TYPE.LIST_KEY_VALUE)
                        print(self.last_recv_data)
                        self.push_to_db(self.last_recv_data)

                except (UnicodeError, AttributeError):
                    # print('recieve not bytes array')
                    pass
            time.sleep(0.001)

    def push_to_db(self, data):
        # todo create sensor_data container(data=2d key value + len)
        for i in range(len(data[0])):
            self.db.lpush(data[0][i], data[1][i])

    def flush_all_db(self):
        self.db.flushdb()


stream_controller = Stream_controller(topic='sensor_mesh')
stream_controller.flush_all_db()
stream_controller.listen()
