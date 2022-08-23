#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

from common.msg import res_put


async def response(client, id, code=0, data=None):
    msg = {
        'type': 'response',
        'id': id,
        'code': code,
        'data': data
    }
    await res_put(client, msg)

