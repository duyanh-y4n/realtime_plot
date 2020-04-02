#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : TimeStamp.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 22.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

import time
# TODO: unittest


class TimeStamp():

    """Docstring for TimeStamp 
    - automatic generate time ticks
    """

    def __init__(self, time_type='millis'):
        self.startTime = time.perf_counter()
        self.time_type = time_type

    def reset(self):
        self.startTime = time.perf_counter()

    def sec(self, round=False):
        if round:
            return int(time.time()-self.startTime+0.5)
        return time.time()-self.startTime

    def millis(self, round=True):
        if round:
            return int(1000*(time.time()-self.startTime)+0.5)
        return 1000*(time.time()-self.startTime)

    def tick(self):
        if self.time_type == 'millis':
            return self.millis()
        else:
            return self.sec()


def time_stamp_test():
    test = TimeStamp()

    time.sleep(0.1)
    print(test.tick())
    test.reset()
    time.sleep(0.1)
    print(test.tick())
    input()


# time_stamp_test()
