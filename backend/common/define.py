#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import sys
import os
from tornado import queues


connected_clients = {}
req_msg_queue = queues.Queue()
res_msg_queue = queues.Queue()

message_processor = None

command = None

PYTHON = sys.executable
PROJECTS = os.path.join(os.path.abspath('.'), 'projects')
if not os.path.exists(PROJECTS):
    os.makedirs(PROJECTS)

subprograms = {}