#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : Dataplot_test.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 22.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>
import unittest
import time
from DataPlot import *
import numpy as np

# random data dimension
while True:
    row = np.random.randint(10)
    col = np.random.randint(10)
    if row > 0 and col > 0:
        break
# row = 2
# col = 3
data_multiple_col = np.random.randint(2, 10)


class DataPlotTimeStampNone(unittest.TestCase):
    def setUp(self):
        # swap col and row to append each new col easily (iterate col through list index)
        self.data = np.random.randint(low=-10, high=10, size=(col, row))
        self.dataplot = DataPlot(
            row, col, option=DataplotOption.TIMESTAMP_NONE)
        for i in range(self.data.shape[0]):
            self.dataplot.append(self.data[i])
        # no swap col and row to extend rows normally
        self.data_multiple = np.random.randint(
            low=-10, high=10, size=(row, data_multiple_col))

    def test_Should_GetCorrectMultipleColumn_When_AppendNewColumns(self):
        # print(self.data_multiple)
        # print(np.array(self.dataplot.get_data_as_matrix()))
        self.dataplot.append(self.data_multiple, single=False)
        # print(np.array(self.dataplot.get_data_as_matrix()))
        # last col of data_multiple and newly updated dataplot should be the same
        self.assertEqual(self.dataplot.get_col(-1),
                         list(self.data_multiple[:, -1]))

    def test_Should_GetCorrectSingleColumn_When_AppendNewColumn(self):
        for i in range(self.data.shape[0]):
            self.assertEqual(list(self.data[i]), self.dataplot.get_col(i))

    def test_Should_GetCorrectSingleRow_When_AppendNewRow(self):
        for i in range(self.data.shape[0]):
            self.assertEqual(list(self.data[i]), self.dataplot.get_col(i))
        while True:
            row = np.random.randint(self.dataplot.row)
            if row >= 0 or row < self.dataplot.row:
                break
        self.assertEqual(list(self.data.transpose()[row]),
                         self.dataplot.get_row(row))


class DataPlotWithTimestampAuto(unittest.TestCase):
    def setUp(self):
        # swap col and row to append each new col easily (iterate col through list index)
        self.data = np.random.randint(low=-10, high=10, size=(col, row))
        self.dataplot = DataPlot(
            row, col, option=DataplotOption.TIMESTAMP_AUTO)
        for i in range(self.data.shape[0]):
            self.dataplot.append(self.data[i])
            time.sleep(0.01)
        # no swap col and row to extend rows normally
        self.data_multiple = np.random.randint(
            low=-10, high=10, size=(row, data_multiple_col))

    def test_Should_GetCorrectSingleColumn_When_AppendNewColumn(self):
        for i in range(self.data.shape[0]):
            self.assertEqual(list(self.data[i]), self.dataplot.get_col(i)[:-1])

    def test_Should_RaiseException_When_AppendNewColumns(self):
        with self.assertRaises(Exception):
            self.dataplot.append(self.data_multiple, single=False)

    def test_Should_GetCorrectSingleRow_When_AppendNewRow(self):
        for i in range(self.data.shape[0]):
            self.assertEqual(list(self.data[i]), self.dataplot.get_col(i)[:-1])
        while True:
            row = np.random.randint(self.dataplot.row)
            if row >= 0 or row < self.dataplot.row:
                break
        self.assertEqual(list(self.data.transpose()[row]),
                         self.dataplot.get_row(row))

    def test_Should_DoNothing_WhenTryingToSortTimeStampCol(self):
        time_row = self.dataplot.get_data_as_matrix()[-1]
        self.assertEqual(time_row, self.dataplot.get_time_ticks())
        sorted_row = time_row
        sorted_row = sorted(time_row, reverse=False)
        self.assertEqual(sorted_row, time_row)


class DataPlotWithTimestampCustom(unittest.TestCase):
    def setUp(self):
        # swap col and row to append each new col easily (iterate col through list index)
        self.data = np.random.randint(low=-10, high=10, size=(col, row))
        self.dataplot = DataPlot(
            row, col, option=DataplotOption.TIMESTAMP_CUSTOM)
        self.timestamp_custom = []
        ticks_start = 0
        ticks_interval = 50
        for i in range(1000):  # 1000 values for time ticks axis (more than enough for now)
            self.timestamp_custom.append(ticks_start + ticks_interval*i)
        for i in range(self.data.shape[0]):
            self.dataplot.append(
                self.data[i], self.timestamp_custom[i], single=True)
        # no swap col and row to extend rows normally
        self.data_multiple = np.random.randint(
            low=-10, high=10, size=(row, data_multiple_col))

    def test_Should_GetCorrectSingleColumn_When_AppendNewColumn(self):
        for i in range(self.data.shape[0]):
            self.assertEqual(list(self.data[i]), self.dataplot.get_col(i)[:-1])

    def test_Should_GetCorrectMultipleColumn_When_AppendNewColumns(self):
        dataplot = DataPlot(
            row, col, option=DataplotOption.TIMESTAMP_CUSTOM)
        dataplot.append(self.data_multiple,
                        x=self.timestamp_custom[:data_multiple_col], single=False)
        self.assertEqual(dataplot.get_col(-1)[:-1],
                         list(self.data_multiple[:, -1]))

    def test_Should_GetCorrectSingleRow_When_AppendNewRow(self):
        for i in range(self.data.shape[0]):
            self.assertEqual(list(self.data[i]), self.dataplot.get_col(i)[:-1])
        while True:
            row = np.random.randint(self.dataplot.row)
            if row >= 0 or row < self.dataplot.row:
                break
        self.assertEqual(list(self.data.transpose()[row]),
                         self.dataplot.get_row(row))

    def test_Should_DoNothing_WhenTryingToSortTimeStampCol(self):
        time_row = self.dataplot.get_data_as_matrix()[-1]
        self.assertEqual(time_row, self.dataplot.get_time_ticks())
        sorted_row = time_row
        sorted_row = sorted(time_row, reverse=False)
        self.assertEqual(sorted_row, time_row)
        print(self.dataplot)


if __name__ == "__main__":
    unittest.main()
