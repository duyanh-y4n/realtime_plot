#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : DataPlot.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 22.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>
from TimeStamp import TimeStamp
from collections import deque
# import numpy as np
from enum import Enum


class DataPlotException(Enum):
    """
    Exception String for Dataplot:
    - Name convention: [ CLASS ]_[ METHODE ]_[ EXCEPTION_NAME ]
    """
    DATAPLOT_APPEND_PARAM_X_NOT_SUPPORTED_BY_OPTION = 'x only available by TIMESTAMP_CUSTOM option'
    DATAPLOT_APPEND_MULTIMODE_UNSUPPORTED_BY_OPTION = 'multimode unsupported by current dataplot option'
    DATAPLOT_APPEND_MULTIMODE_X_AND_Y_DIFF_LEN = 'x and y do not have the same length'
    DATAPLOT_APPEND_MULTIMODE_X_NONE_BY_TIMESTAMP_CUSTOM = 'x cant be None by TIMESTAMP_CUSTOM option'
    DATAPLOT_GET_TIME_TICKS_NOT_AVAILABLE = 'time ticks not available by option TIMESTAMP_NONE'


class DataplotOption(Enum):
    TIMESTAMP_NONE = 0 # x axis as numerical
    TIMESTAMP_AUTO = 1 # x axis as autogenated time ticks (time when new data appended)
    TIMESTAMP_CUSTOM = 2 # x axis as time ticks (time ticks generated from outside and added as parameter)


class DataPlot(object):

    """Docstring for DataPlot.
    - Container for Data (e.g. Data from multiple sensor)
    - implement as deque(works like shift register or FIFO)
    - all data must have the same x-axis !!
    """

    def __init__(self, row=1, col=20, option=DataplotOption.TIMESTAMP_AUTO.value, time_type='millis'):
        """Constructor

        @param row: y axis data ~ data for 1 measurand
        @param col: x axis data ~ data reading point (numerical or time ticks in seconds or milliseconds)
        @param option: timestamp enable/disable auto/custom
        @param row: y data ~ data for 1 measurand

        @return:  Description
        @rtype :  Type

        @raise e:  Description
        """
        self.row = row
        self.col = col
        self.data_regs = []
        self.time_ticks = []
        # TODO: use numpy to save data in matrix
        self.data = []
        for i in range(row):
            self.data_regs.append(deque(maxlen=col))
        self.option = option
        if self.option == DataplotOption.TIMESTAMP_AUTO.value:
            self.timestamp = TimeStamp(time_type=time_type)
            self.time_ticks = deque(maxlen=col)
        if self.option == DataplotOption.TIMESTAMP_CUSTOM.value:
            self.time_ticks = deque(maxlen=col)

    def __str__(self):
        self.get_data_as_matrix()
        if self.option == DataplotOption.TIMESTAMP_AUTO.value or self.option == DataplotOption.TIMESTAMP_CUSTOM.value:
            ret = 'data: ' + str(self.data[:-1])
        # last row are time ticks
            ret = ret + ('\ntime: ' + str(self.data[-1]))
        elif self.option == DataplotOption.TIMESTAMP_NONE.value:
            ret = 'data: ' + str(self.data)
        return ret

    def append(self, y, x=None, single=True):
        """append new data vector to class

        @param y:  vector y=[y0, y1, y2, ...] or matrix y=[y00 y01 y02, y10 y11 y12, ...]
        @type  param:  list

        """
        if self.option != DataplotOption.TIMESTAMP_CUSTOM.value and x != None:
            raise Exception(
                DataPlotException.DATAPLOT_APPEND_PARAM_X_NOT_SUPPORTED_BY_OPTION.value)
        if single:
            for i in range(self.row):
                self.data_regs[i].append(y[i])
            if self.option == DataplotOption.TIMESTAMP_AUTO.value:
                self.time_ticks.append(self.timestamp.tick())
            if self.option == DataplotOption.TIMESTAMP_CUSTOM.value:
                self.time_ticks.append(x)
        else:  # multi mode
            for i in range(self.row):
                self.data_regs[i].extend(y[i])
            if self.option == DataplotOption.TIMESTAMP_AUTO.value:
                # not supported be cause timestamp can generate multiple ticks but it make no sense
                raise Exception(
                    DataPlotException.DATAPLOT_APPEND_MULTIMODE_UNSUPPORTED_BY_OPTION.value)
            if self.option == DataplotOption.TIMESTAMP_CUSTOM.value:
                if x == None:
                    raise Exception(
                        DataPlotException.DATAPLOT_APPEND_MULTIMODE_X_NONE_BY_TIMESTAMP_CUSTOM.value)
                if len(x) != len(y[0]):
                    raise Exception(
                        DataPlotException.DATAPLOT_APPEND_MULTIMODE_X_AND_Y_DIFF_LEN.value)
                self.time_ticks.extend(x)

    def get_data_as_matrix(self):
        """get data as 2d list (last row will be time ticks if timestamp enable)

        """
        self.data = []
        for i in range(self.row):
            self.data.append(list(self.data_regs[i]))
        if self.option == DataplotOption.TIMESTAMP_AUTO.value or self.option == DataplotOption.TIMESTAMP_CUSTOM.value:
            self.data.append(list(self.time_ticks))
        return self.data

    def get_col(self, index):
        """get data vector at specific index as list

        @param index:  col index
        """
        ret = []
        for i in range(self.row):
            ret.append(list(self.data_regs[i])[index])
        if self.option == DataplotOption.TIMESTAMP_AUTO.value or self.option == DataplotOption.TIMESTAMP_CUSTOM.value:
            ret.append(list(self.time_ticks)[index])
        return ret

    def get_row(self, index):
        """get row data (measurand's y_data) as list

        @param index:  row index
        """
        return list(self.data_regs[index])

    def get_time_ticks(self):
        if self.option == DataplotOption.TIMESTAMP_NONE:
            raise Exception(
                DataPlotException.DATAPLOT_GET_TIME_TICKS_NOT_AVAILABLE.value)
        return list(self.time_ticks)
