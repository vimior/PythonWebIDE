#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import json
from tornado import queues

REQ_QUE = queues.Queue()
RES_QUE = queues.Queue()


class RequestItem(object):
    def __init__(self, client, msg) -> None:
        self.client = client
        self._data = msg if isinstance(msg, dict) else json.loads(msg)

    @property
    def data(self):
        return self._data


class ResponseItem(object):
    def __init__(self, client, msg) -> None:
        self.client = client
        self._data = json.dumps(msg) if isinstance(msg, dict) else msg

    @property
    def data(self):
        return self._data


async def req_put(client, msg):
    item = RequestItem(client, msg)
    return await REQ_QUE.put(item)


async def res_put(client, msg):
    item = ResponseItem(client, msg)
    return await RES_QUE.put(item)


async def req_get(timeout=None):
    return await REQ_QUE.get(timeout=timeout)


async def res_get(timeout=None):
    return await RES_QUE.get(timeout=timeout)

