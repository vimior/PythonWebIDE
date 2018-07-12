#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import json
from tornado import gen
from . import define


@gen.coroutine
def push_req_queue(client, msg, is_json=False):
    try:
        if not is_json:
            msg = json.loads(msg)
        item = {
            'client': client,
            'data': msg
        }
        yield define.req_msg_queue.put(item)
    except:
        pass


@gen.coroutine
def push_res_queue(client, msg):
    try:
        item = {
            'client': client,
            'data': msg
        }
        yield define.res_msg_queue.put(item)
    except:
        pass

