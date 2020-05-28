#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : RealtimePlotter_example.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 02.04.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

from RealtimePlotter import *
from RealtimeDataMessage import *
import redis
import numpy as np


row = 3
col = 200
plot_update_interval = 0.005

option = DataplotOption.TIMESTAMP_CUSTOM
# option = DataplotOption.TIMESTAMP_NONE
dataplot = DataPlot(row, col, option=option)

realtimeplotter = RealtimePlotter(dataplot)

msgParser = MessageParser()

datasource = redis.StrictRedis(host='localhost', port=6379, db=0)

# define data to get from db
sensorMeshList = ['sensor0', 'sensor1', 'sensor2', 'sensor3']
if(dataplot.option == DataplotOption.TIMESTAMP_CUSTOM):
    # add time to data list (see SensorMeshSim_example)
    sensorMeshList.append('sensor4')
print(sensorMeshList)

fig, axes = plt.subplots()
plt.title('Data Live Stream with redis')
# plt.show()

realtimeplotter.config_plots(axes, ylim=[-2, 2])
while True:
    # clear all cached (inc. corrupted data)
    realtimeplotter.dataplot.clear_data_regs()

    # get new data from database
    new_data = []
    for sensor in sensorMeshList:
        new_sensor_data = datasource.lrange(sensor, 0, col)
        # reverse, bc first element is the newest (not the oldest like deque)
        new_sensor_data.reverse()
        # print(sensor + ':')
        # print(new_sensor_data)
        new_data.append(new_sensor_data)
    # print(np.array(new_data, dtype=np.float))

    # plot data
    try:
        if realtimeplotter.dataplot.option == DataplotOption.TIMESTAMP_NONE:
            new_data = np.array(new_data, dtype=np.float)
            realtimeplotter.dataplot.append(
                new_data, single=False)
        elif realtimeplotter.dataplot.option == DataplotOption.TIMESTAMP_CUSTOM:
            y = np.array(new_data[:-1], dtype=np.float)
            x = np.array(new_data[-1], dtype=np.int64)
            realtimeplotter.dataplot.append(
                y=y, x=x, single=False)
        realtimeplotter.plot_data()
    except Exception:
        pass
    plt.pause(plot_update_interval)
input("Exit(press any key)?")
