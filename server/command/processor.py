#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

from common.msg import req_get, res_get, res_put, REQ_QUE, RES_QUE
from .command import Command
from utils.log import logger


class RequestProcessor(object):
    def __init__(self) -> None:
        self._command = Command()

    async def _process(self, item):
        cmd = item.data.get('cmd', None)

        if hasattr(self._command, cmd):
            logger.info('cmd: {}'.format(cmd))
            func= getattr(self._command, cmd)
            await func(item.client, item.data.get('cmd_id', item.data.get('id', 0)), item.data.get('data', {}))
        else:
            logger.error('cmd %s is not exists'.format(cmd))
            msg = {
                'type': 'response',
                'id': item.data.get('cmd_id', item.data.get('id', 0)),
                'code': 1000,
                'data': 'not support cmd: {}'.format(cmd)
            }
            await res_put(item.client, msg)

    async def loop(self):
        print('request processor loop')
        while True:
            try:
                item = await req_get()
                await self._process(item)
                REQ_QUE.task_done()
            except Exception as e:
                print('request processor ex: {}'.format(e))


class ResponseProcessor(object):
    def __init__(self) -> None:
        pass

    async def _process(self, item):
        if item.client and item.client.connected:
            item.client.write_message(item.data)

    async def loop(self):
        print('response processor loop')
        while True:
            try:
                item = await res_get()
                await self._process(item)
                RES_QUE.task_done()
            except Exception as e:
                print('response processor ex: {}'.format(e))




