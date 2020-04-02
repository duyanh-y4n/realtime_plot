#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : RealtimePlotter.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 23.03.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>
from DataPlot import *
import matplotlib.pyplot as plt
import numpy as np

# TODO: use enum for exceptions


class RealtimePlotter(object):

    """Docstring for RealtimePlotter. """

    def __init__(self, dataplot):
        """TODO: to be defined.

        :TODO: TODO

        """
        if dataplot.__class__.__name__ == 'DataPlot':
            self.dataplot = dataplot
        else:
            raise TypeError('dataplot not type class DataPlot')

    def config_plots(self, axes, y_labels=[], ylim=[], x_label=''):
        self.axes = axes
        # TODO: implement numpy in dataplot.py
        data = np.array(self.dataplot.get_data_as_matrix())
        # print('data')
        # print(data)
        # set limits
        # TODO: auto ylim (cause bug, not work yet!!)
        if ylim == [] and self.dataplot.option in [DataplotOption.TIMESTAMP_AUTO, DataplotOption.TIMESTAMP_CUSTOM]:
            # last row is x-axis and wont be counted
            ylim = [
                np.min(data[:-1]),
                np.max(data[:-1])
            ]
        elif ylim == [] and self.dataplot.option == DataplotOption.TIMESTAMP_NONE:
            ylim = [
                np.min(data[:])*0.9,
                np.max(data[:])*1.1
            ]
        # print(ylim)
        self.axes.set_ylim(ylim)
        self.lines = []
        # set labels and legends
        # if y_labels == []:
        if len(y_labels) != self.dataplot.row:
            self.y_labels = []
            for i in range(self.dataplot.row):
                self.y_labels.append('sensor '+str(i))
        else:
            self.y_labels = y_labels
        if x_label == '' and self.dataplot.option == DataplotOption.TIMESTAMP_AUTO:
            self.axes.set_xlabel(
                'time in ' + self.dataplot.timestamp.time_type)
        elif x_label == '' and self.dataplot.option == DataplotOption.TIMESTAMP_NONE:
            self.axes.set_xlabel('n. measurement(0 = oldest in queue)')
        elif x_label == '' and self.dataplot.option == DataplotOption.TIMESTAMP_CUSTOM:
            self.axes.set_xlabel('time(custom)')
        else:
            self.axes.set_xlabel(x_label)
        for i in range(self.dataplot.row):
            line, = self.axes.plot([], [], label=self.y_labels[i])
            self.lines.append(line)
        self.axes.relim()
        self.axes.legend(loc='upper left')

    def plot_data(self):
        if self.dataplot.option in [DataplotOption.TIMESTAMP_AUTO, DataplotOption.TIMESTAMP_CUSTOM]:
            x = np.array(self.dataplot.get_time_ticks())
            for i in range(self.dataplot.row):
                y = np.array(self.dataplot.get_row(i))
                self.lines[i].set_data(x, y)
                # print(x)
                # print(self.dataplot.get_row(i))
        elif self.dataplot.option == DataplotOption.TIMESTAMP_NONE:
            # update left
            # x = np.arange(len(self.dataplot.get_row(0)))*-1

            # update right
            x = np.arange(len(self.dataplot.get_row(0)))

            # print(x)
            for i in range(self.dataplot.row):
                y = np.array(self.dataplot.get_row(i))
                self.lines[i].set_data(x, y)
                # print(y)
        try:
            self.axes.set_xlim(np.min(x), np.max(x))
        except ValueError:
            # except error when Database leer or no data available yet
            pass
        self.axes.relim()
