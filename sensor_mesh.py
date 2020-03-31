#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : sensor_mesh.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 31.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

# -*- coding: utf-8 -*-
"""
    realtime_sensor_plot.sensor_mesh
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    simulate sensor mesh data and push to redis stream

    :copyright: (c) 2020 by Duy Anh Pham.
    :license: MIT, see LICENSE for more details.
"""
# from __future__ import absolute_import
from RealtimeDataMessage import *
import time
import redis
import numpy as np
# from sys import path
# sys.path.insert(0, '../../lib')

max_len = 10000
data_sample = np.sin(np.arange(0, max_len, 1)*np.pi/180)
ticks_interval = 50
ticks_start = 100
# time_ticks = np.arange(0, max_len, 1)*ticks_interval


class Sensor_mesh():

    def __init__(self, sensor_num=3, noise=10, topic='sensor_mesh'):
        """__init__.

        :param sensor_num:
        :param noise: signal noise in %
        """
        self.sensor_num = sensor_num
        self.new_data = []
        self.iterator = 0
        self.noise = noise
        self.stream = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.topic = topic
        self.messageParser = MessageParser()
        self.runtime = ticks_start

    def update(self, with_time=False):
        # periodic iterate through data_sample
        self.iterator = (self.iterator+1) % max_len
        self.new_data.clear()
        for i in range(self.sensor_num):
            direction = (-1)**i
            noise = np.random.randint(-self.noise, self.noise)
            self.new_data.append(
                data_sample[self.iterator]*(1.0+noise/100))
        if with_time:
            self.new_data.append(self.runtime)
        self.runtime = self.runtime + ticks_interval
        # data_sample[self.iterator]*1.1)
        # print(self.new_data)
        return self.new_data

    def push_to_stream(self, data):
        msg = self.messageParser.encode(
            header=MessageFormatHeader.HEADER_DATA, values=data)
        print(msg)
        self.stream.publish(self.topic, msg)


sensor = Sensor_mesh()
for i in range(100):
    data = sensor.update(with_time=True)
    sensor.push_to_stream(data)
