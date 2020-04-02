#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : SensorMeshSim_example.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 02.04.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

from SensorMeshSim import *


sensorMesh = SensorMeshSim()
sensorMesh.set_sensor_num(4)
for i in range(1000):
    data = sensorMesh.update(with_time=True)
    print('-topic- ' + sensorMesh.topic)
    print('-data- ')
    msg = sensorMesh.push_to_stream(data)
    print(msg)
    time.sleep(0.01)
