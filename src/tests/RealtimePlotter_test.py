#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : RealtimePlotter_test.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 23.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>
import unittest
import matplotlib.pyplot as plt
import numpy as np
from RealtimePlotter import *
import time

# TODO:
#   - TestCase for setting labels

# random dataplot dimension
while True:
    row = np.random.randint(10)
    col = np.random.randint(20, 50)
    if row > 0 and col > 0:
        break

# random data source
data_len = 100
data_interval = 0.005
plot_update_interval = 0.01
datasource = np.random.randint(
    low=-10, high=10, size=(data_len, row))


class RealtimePlotterClassTest(unittest.TestCase):
    def setUp(self):
        self.data = np.random.randint(low=-10, high=10, size=(col, row))
        self.dataplot = DataPlot(
            row, col, option=DataplotOption.TIMESTAMP_NONE)

    def tearDown(self):
        # tear down code
        pass


class PlottingTest(unittest.TestCase):
    def setUp(self):
        pass

    # all plots should look the same
    def test_Should_UpdateDataRealtimeWithCustomTimestamp_When_GettingDataFromSource(self):
        # test code:
        #           good use case when time ticks saved in 3rd-party database/cached memory.
        #           use plt.pause in separated process
        #           update data in database
        dataplot = DataPlot(
            row, col, option=DataplotOption.TIMESTAMP_CUSTOM)
        # simulating time ticks that saved in DB/cahed memory
        self.timestamp_custom = []
        ticks_start = 0
        ticks_interval = 50
        for i in range(1000):  # 1000 values for time ticks axis (more than enough for now)
            self.timestamp_custom.append(ticks_start + ticks_interval*i)
        self.realtimeplotter = RealtimePlotter(dataplot)
        fig, axes = plt.subplots()
        plt.title('Plotting Data')
        # plt.show()
        self.realtimeplotter.config_plots(axes, ylim=[-11, 11])
        for i in range(datasource.shape[0]):
            self.realtimeplotter.dataplot.append(
                datasource[i], self.timestamp_custom[i])
            self.realtimeplotter.plot_data()
            plt.pause(plot_update_interval)
        print(dataplot)
        input("Continue(press any key)?")

    def test_Should_UpdateDataRealtimeWithTimestamp_When_GettingDataFromSource(self):
        # test code:
        #           not good use case because blocking process cause additional delays.
        #           use plt.pause in separated process
        #           update data in database
        dataplot = DataPlot(
            row, col, option=DataplotOption.TIMESTAMP_AUTO)
        self.realtimeplotter = RealtimePlotter(dataplot)
        fig, axes = plt.subplots()
        plt.title('Plotting Data')
        # plt.show()
        self.realtimeplotter.config_plots(axes, ylim=[-11, 11])
        for i in range(datasource.shape[0]):
            self.realtimeplotter.dataplot.append(datasource[i])
            # time ticks auto. generated base on delays interval
            time.sleep(data_interval)
            self.realtimeplotter.plot_data()
            plt.pause(plot_update_interval)
        input("Continue(press any key)?")

    def test_Should_UpdateDataRealtimeWithoutTimestamp_When_GettingDataFromSource(self):
        # test code:
        #           not good use case because blocking process cause performances delays.
        #           use plt.pause in separated process
        #           update data in database
        dataplot = DataPlot(
            row, col, option=DataplotOption.TIMESTAMP_NONE)
        self.realtimeplotter = RealtimePlotter(dataplot)
        fig, axes = plt.subplots()
        plt.title('Plotting Data')
        # plt.show()
        self.realtimeplotter.config_plots(
            axes, y_labels=['a', 'b', 'c'], ylim=[-11, 11])
        for i in range(datasource.shape[0]):
            self.realtimeplotter.dataplot.append(datasource[i])
            self.realtimeplotter.plot_data()
            plt.pause(plot_update_interval)
        input("Continue(press any key)?")

    def tearDown(self):
        # tear down code
        pass
