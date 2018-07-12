#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

from tornado import gen
from command import Command
from . import define


class MessageProcessor(object):
    def __init__(self):
        define.command = Command()

    @gen.coroutine
    def process_message(self, client, msg):
        cmd = msg.get('cmd')
        if hasattr(define.command, cmd):
            func = getattr(define.command, cmd)
            yield func(client, msg['id'], msg.get('data', {}))
        else:
            res = {
                'type': 'response',
                'id': msg['id'],
                'code': 1000,
                'data': 'not support cmd: {}'.format(cmd)
            }
            raise gen.Return(res)

