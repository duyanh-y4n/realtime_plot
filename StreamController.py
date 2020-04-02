#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : StreamController.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 31.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

import redis
import time
from RealtimeDataMessage import *
from enum import Enum
from SensorMeshBase import SensorMeshUpstream


class StreamControllerException(Enum):
    """
    Exception String for StreamController:
    - Name convention: [ CLASS ]_[ METHODE ]_[ EXCEPTION_NAME ]
    """
    STREAMCONTROLLER_SET_DOWNSTREAM_INVALID = 'Downstream invalid'
    STREAMCONTROLLER_SET_DATABASE_INVALID = 'Database invalid'


class StreamServer(Enum):
    REDIS = 0
    # TODO: KAFKA,MONGO,MYSQL


class StreamController():
    def __init__(self, topic, downstream=SensorMeshUpstream.REDIS, database=StreamServer.REDIS):
        self.downstream = None
        self.downstream_option = None
        self.set_downstream(downstream)
        self.database_option = None
        self.database = None
        self.set_database(database)
        self.topic = topic
        self.pubsub.subscribe(self.topic)
        self.msgParser = MessageParser()
        self.last_recv_data = []

    def set_downstream(self, downstream):
        if downstream == SensorMeshUpstream.REDIS:
            self.downstream_option = StreamServer.REDIS
            self.downstream = redis.StrictRedis(
                host='localhost', port=6379, db=0)
            self.pubsub = self.downstream.pubsub()
        else:
            raise Exception(
                StreamControllerException.STREAMCONTROLLER_SET_DOWNSTREAM_INVALID)

    def set_database(self, database):
        if database == StreamServer.REDIS:
            self.database_option = StreamServer.REDIS
            self.database = redis.StrictRedis(
                host='localhost', port=6379, db=0)
        else:
            raise Exception(
                StreamControllerException.STREAMCONTROLLER_SET_DATABASE_INVALID)

    def listen(self):
        while True:
            self.get_message()
            time.sleep(0.001)

    def get_message(self):
        """get_message.
        - get message from stream and push to database"""
        if self.downstream_option == StreamServer.REDIS:
            msg = self.pubsub.get_message()
            if msg:
                rec = False
                try:
                    rec = msg.get('data').decode('utf-8')  # remove b' encoding
                    if self.msgParser.decode(rec, ret_type=RET_TYPE.LIST_KEY_VALUE) != False:
                        self.last_recv_data = self.msgParser.decode(
                            rec, ret_type=RET_TYPE.LIST_KEY_VALUE)
                        print(self.last_recv_data)
                        self.push_to_database(self.last_recv_data)

                except (UnicodeError, AttributeError):
                    # print('recieve not bytes array')
                    pass

    def push_to_database(self, data):
        # TODO: create sensor_data container(data=2d key value + len)
        if self.database_option == StreamServer.REDIS:
            for i in range(len(data[0])):
                self.database.lpush(data[0][i], data[1][i])
        else:
            raise Exception(
                StreamControllerException.STREAMCONTROLLER_SET_DATABASE_INVALID)

    def flush_all_database(self):
        if self.database_option == StreamServer.REDIS:
            self.database.flushdb()
        else:
            raise Exception(
                StreamControllerException.STREAMCONTROLLER_SET_DATABASE_INVALID)

