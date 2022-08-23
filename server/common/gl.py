#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import os
import sys
from tornado import queues

class GLOBAL:
    class Queue:
        req_msg_que = queues.Queue()
        res_msg_que = queues.Queue()

    class Path:
        PYTHON = sys.executable
        PROJECTS = os.path.join(os.path.abspath('.'), 'projects')


