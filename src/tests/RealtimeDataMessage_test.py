#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : RealtimeDataMessage_test.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 28.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>
import unittest
import numpy as np
from RealtimeDataMessage import *

test_sensor = DEFAULT_DEVICE_NAME
sensor_num = np.random.randint(3, 10)
random_msg_num = np.random.randint(5, 10)
test_value = [1, -1]
test_device = ['baro', 'tof']
test_default_device = [DEFAULT_DEVICE_NAME, DEFAULT_DEVICE_NAME]
test_msg = 'data;baro:1:tof:-1:'
test_msg_none_device = 'data;sensor0:1:sensor1:-1:'


class TestMessageParser(unittest.TestCase):
    def setUp(self):
        self.msgs = []
        # add predefined messages:
        for msg in MESSAGES:
            self.msgs.append(msg.value)
        # generate random messages for sensor data
        for i in range(random_msg_num):
            new_msg = MessageFormatHeader.HEADER_DATA.value + \
                MessageFormatSeparator.SEPARATOR_HEAD.value
            for j in range(sensor_num):
                new_msg = new_msg + test_sensor + str(j) + MessageFormatSeparator.SEPARATOR_BODY.value + str(
                    np.random.randint(-10, 10)) + MessageFormatSeparator.SEPARATOR_BODY.value
            self.msgs.append(new_msg)
        # print(self.msgs)
        self.msgParser = MessageParser()

    def test_Should_CheckTrue_When_MessageHeaderIsCorrect(self):
        for msg in self.msgs:
            self.assertTrue(self.msgParser.check(msg))
            self.assertNotEqual(self.msgParser.last_msg, msg)

    def test_Should_CheckTrueAndSaveLastMsg_When_MessageHeaderIsCorrect(self):
        for msg in self.msgs:
            self.assertTrue(self.msgParser.check(msg, save_msg=True))
            self.assertEqual(self.msgParser.last_msg, msg)

    def test_Should_EncodeCorectly_When_EncodingNormalDataMsg(self):
        msg = self.msgParser.encode(
            header=MessageFormatHeader.HEADER_DATA, labels=test_device, values=test_value)
        # print(msg)
        self.assertEqual(msg, test_msg)
        msg = self.msgParser.encode(
            header=MessageFormatHeader.HEADER_DATA, values=test_value)
        self.assertEqual(msg, test_msg_none_device)
        # print(msg)

    def test_Should_DecodeCorectly_When_InputNormalDataMsg(self):
        msg = self.msgParser.encode(
            header=MessageFormatHeader.HEADER_DATA, values=test_value)
        self.assertEqual(msg, test_msg_none_device)
        # print(msg)
        ret_type_sep = self.msgParser.decode(
            msg, ret_type=RET_TYPE.LIST_SEPARATED)
        # print(ret_type_sep)
        ret_type_hash = self.msgParser.decode(
            msg, ret_type=RET_TYPE.LIST_KEY_VALUE)
        # print(ret_type_hash)
        self.assertEqual(ret_type_sep[1], ret_type_hash[0][0])
        self.assertEqual(ret_type_sep[2], ret_type_hash[1][0])
        self.assertEqual(ret_type_sep[-2], ret_type_hash[0][-1])
        self.assertEqual(ret_type_sep[-1], ret_type_hash[1][-1])

        ret_type_dict = self.msgParser.decode(
            msg, ret_type=RET_TYPE.DICT)
        # print(ret_type_dict)
        self.assertEqual(list(ret_type_dict.keys()), self.msgParser.keys)
        self.assertEqual(list(ret_type_dict.values()), self.msgParser.values)

    def test_Should_ReturnFalse_When_DecodingUndefinedMessage(self):
        wrong_msg = 'random messages'
        true_msg = 'ack;'
        self.assertEqual(False, self.msgParser.decode(wrong_msg))
        self.assertNotEqual(False, self.msgParser.decode(true_msg))

    def tearDown(self):
        pass
