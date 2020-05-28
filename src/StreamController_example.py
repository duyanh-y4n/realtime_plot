#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File            : StreamController_example.py
# Author          : Duy Anh Pham <duyanh.y4n.pham@gmail.com>
# Date            : 02.04.2020
# Last Modified By: Duy Anh Pham <duyanh.y4n.pham@gmail.com>

from StreamController import *


stream_controller = StreamController(topic='sensor_mesh')
stream_controller.flush_all_database()
stream_controller.listen()
