#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : RealtimeDataMessage.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 28.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

from enum import Enum

"""
simple realtime data message format:
    |header;sensor1:data1:sensor2:data2:sensor3:data3:....|
"""

DEFAULT_DEVICE_NAME = 'sensor'


class MessageFormatHeader(Enum):
    HEADER_DATA = 'data'
    HEADER_ACK = 'ack'
    HEADER_NACK = 'nack'


class MessageFormatMarker(Enum):
    MARKER_BARO = 'baro'
    MARKER_TOF = 'tof'
    MARKER_IMU_X = 'imu_x'
    MARKER_IMU_Y = 'imu_y'
    MARKER_IMU_Z = 'imu_z'


class MessageFormatSeparator(Enum):
    SEPARATOR_HEAD = ';'
    SEPARATOR_BODY = ':'


class MESSAGES(Enum):
    ACK = 'ack;'
    NACK = 'nack;'


class RET_TYPE(Enum):
    LIST_SEPARATED = 0
    LIST_KEY_VALUE = 1
    DICT = 2


class MessageParser(object):

    """Docstring for MessageFormatter. """

    def __init__(self):
        self.last_msg = 'None'
        self.last_decoded_msg = 'None'
        self.keys = []
        self.values = []

    def check(self, msg, save_msg=False):
        decoded_msg = msg.replace(';', ':').split(':')
        if save_msg:
            # last element is abundant
            self.last_decoded_msg = decoded_msg[:-1]
            self.last_msg = msg
        check = False
        for header in MessageFormatHeader:
            if decoded_msg[0] == header.value:
                return True
        return check

    def decode(self, message, ret_type=RET_TYPE.LIST_KEY_VALUE):
        if self.check(message, save_msg=True) == False:
            return False
        self.keys.clear()
        self.values.clear()
        for i in range(1, len(self.last_decoded_msg), 2):
            self.keys.append(self.last_decoded_msg[i])
            self.values.append(self.last_decoded_msg[i+1])
        if ret_type == RET_TYPE.LIST_SEPARATED:
            return self.last_decoded_msg
        elif ret_type == RET_TYPE.LIST_KEY_VALUE:
            return [self.keys, self.values]
        elif ret_type == RET_TYPE.DICT:
            ret = {}
            for i in range(len(self.keys)):
                ret[self.keys[i]] = self.values[i]
            return ret

    def encode(self, header, values, labels=None):
        new_msg = header.value + \
            MessageFormatSeparator.SEPARATOR_HEAD.value
        if labels == None:
            for i in range(len(values)):
                new_msg = new_msg + DEFAULT_DEVICE_NAME + str(i) + MessageFormatSeparator.SEPARATOR_BODY.value + str(values[i]) \
                    + MessageFormatSeparator.SEPARATOR_BODY.value
        elif labels != None and len(labels) == len(values):
            for i in range(len(labels)):
                new_msg = new_msg + labels[i] + MessageFormatSeparator.SEPARATOR_BODY.value + str(values[i]) \
                    + MessageFormatSeparator.SEPARATOR_BODY.value
        else:
            # print(labels)
            # print(values)
            raise IndexError('labels len and values len not the same')
        return new_msg
