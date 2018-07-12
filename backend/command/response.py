#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

from tornado import gen
from common.utils import push_res_queue


@gen.coroutine
def response(client, id, code=0, data=None):
    res = {
        'type': 'response',
        'id': id,
        'code': code,
        'data': data
    }
    yield push_res_queue(client, res)

