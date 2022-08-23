#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import datetime
from tornado import websocket
from tornado import ioloop
import tornado.web
from tornado import gen, httputil
from typing import Optional, Awaitable, Union, Any
from utils.log import logger
from common.msg import req_put
from .handler_info import HandlerInfo

class WebSocketHandler(websocket.WebSocketHandler):
    def __init__(self, application: tornado.web.Application, request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.connected = False
        self.handler_info = HandlerInfo()
    
    @property
    def id(self):
        return id(self)
    
    def check_origin(self, origin: str) -> bool:
        # return super().check_origin(origin)
        return True

    def open(self, *args: str, **kwargs: str) -> Optional[Awaitable[None]]:
        # return super().open(*args, **kwargs)
        self.connected = True
        self.set_nodelay(True)
        logger.debug('websocket client opened, ip={}, id={}, {}'.format(self.request.remote_ip, id(self), datetime.datetime.now()))

    def on_close(self) -> None:
        # return super().on_close()
        self.connected = False
        logger.debug('Websocket client closed, ip={}, id={}, {}'.format(self.request.remote_ip, id(self), datetime.datetime.now()))

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:
        # return super().on_message(message)
        self._run_callback(req_put, self, message)
    
    @staticmethod
    def _run_callback(callback, *args, **kwargs):
            try:
                result = callback(*args, **kwargs)
            except Exception as e:
                logger.error('run_callback error, {}'.format(e))
                return None
            else:
                if result is not None:
                    result = gen.convert_yielded(result)
                    ioloop.IOLoop.current().add_future(result, lambda f: f.result())
                return result