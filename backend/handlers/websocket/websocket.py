#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import threading
import queue
import time
import datetime
from tornado import gen
from tornado import websocket
from utils.log import logger
from common.utils import push_req_queue


class WebSocketHandler(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(WebSocketHandler, self).__init__(*args, **kwargs)
        self._info = {}
        self._connected = False

    @property
    def connected(self):
        return self._connected

    @property
    def info(self):
        return self._info

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def open(self, *args, **kwargs):
        self._info['type'] = self.get_argument('type', 'cmd')
        self._info['remote_ip'] = self.request.remote_ip
        self._info['id'] = id(self)
        self._connected = True
        logger.debug('A new ws client [type:{}] [id:{}] [addr:{}], {}'.format(
            self.info['type'],
            self.info['id'],
            self.info['remote_ip'],
            datetime.datetime.now()))

    def on_close(self):
        self._connected = False
        logger.debug('ws client [type:{}] [id:{}] [addr:{}], closed on {}'.format(
            self.info['type'],
            self.info['id'],
            self.info['remote_ip'],
            datetime.datetime.now()))

    def on_message(self, message):
        if self.info['type'] == 'cmd':
            push_req_queue(self, message)



