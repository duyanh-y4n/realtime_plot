#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : SensorMeshBase.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 02.04.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

from enum import Enum
import redis
# from RealtimeDataMessage import *
from .RealtimeDataMessage import *


class SensorMeshBaseException(Enum):
    """
    Exception String for SensorMeshBase:
    - Name convention: [ CLASS ]_[ METHODE ]_[ EXCEPTION_NAME ]
    """
    SENSORMESHBASE_SET_UPSTREAM_INVALID = 'Upstream not invalid'
    SENSORMESHBASE_SET_DATABASE_INVALID = 'Database not invalid'


class SensorMeshUpstream(Enum):
    REDIS = 0
    # TODO: MQTT, Kafka,...


class SensorMeshBase():
    """SensorMeshBase.
    Base Class for abstracted IOT Sensor Mesh network
    attr:
        - topic
        - sensor_num
        - upstream
        - upstream_option
        - messageParser
        - new_data: contain last updated data
    """

    def __init__(self):
        self.topic = 'sensor_mesh'
        self.sensor_num = 0
        self.upstream = None
        self.upstream_option = None
        self.messageParser = MessageParser()
        self.set_upstream(SensorMeshUpstream.REDIS)
        self.new_data = []
        pass

    def update(self, with_time=False):
        """update.
        update sensors data as vector/list

        :param with_time: should be check if new_data contain timestamp/runtime information
        """
        raise Exception('not yet implement')

    def push_to_stream(self, data):
        msg = self.messageParser.encode(
            header=MessageFormatHeader.HEADER_DATA, values=data)
        if self.upstream_option == SensorMeshUpstream.REDIS:
            self.upstream.publish(self.topic, msg)
            return msg
        else:
            raise Exception(
                SensorMeshBaseException.SENSORMESHBASE_SET_UPSTREAM_INVALID.value)

    def set_upstream_topic(self, topic):
        self.topic = topic

    def set_sensor_num(self, sensor_num):
        self.sensor_num = sensor_num

    def set_upstream(self, upstream):
        if upstream == SensorMeshUpstream.REDIS:
            self.upstream_option = SensorMeshUpstream.REDIS
            self.upstream = redis.StrictRedis(
                host='localhost', port=6379, db=0)
        else:
            raise Exception(
                SensorMeshBaseException.SENSORMESHBASE_SET_UPSTREAM_INVALID.value)
