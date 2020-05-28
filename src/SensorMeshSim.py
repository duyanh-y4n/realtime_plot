#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : SensorMeshSim.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 31.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

# from __future__ import absolute_import
from SensorMeshBase import *
import time
import numpy as np

max_len = 10000
data_sample = np.sin(np.arange(0, max_len, 1)*np.pi/180)
ticks_interval = 50
ticks_start = 100
# time_ticks = np.arange(0, max_len, 1)*ticks_interval


class SensorMeshSim(SensorMeshBase):
    """
    Simulation Class for abstracted IOT Sensor Mesh network (for testing)
    """

    def __init__(self):
        super().__init__()
        self.iterator = 0
        self.noise = 10
        self.runtime = ticks_start

    def update(self, with_time=False):
        """update.

        :param with_time: True if last sensor is a timer, which generate timestamp
        """
        # periodic iterate through data_sample
        self.iterator = (self.iterator+1) % max_len
        self.new_data.clear()
        for i in range(self.sensor_num):
            direction = (-1)**i
            noise = np.random.randint(-self.noise, self.noise)
            self.new_data.append(
                data_sample[self.iterator]*(1.0+noise/100))
        if with_time:  # last sensor is timer, which generate timestamp
            self.new_data.append(self.runtime)
        self.runtime = self.runtime + ticks_interval
        # data_sample[self.iterator]*1.1)
        # print(self.new_data)
        return self.new_data

    def set_signal_noise_ratio(self, noise=10):
        """set_signal_noise_ratio.

        :param noise: simulate SNR
        """
        self.noise = noise
