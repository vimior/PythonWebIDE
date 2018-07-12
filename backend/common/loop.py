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
from . import processor

define.message_processor = processor.MessageProcessor()


@gen.coroutine
def process_req_loop():
    print('process req loop start')
    while True:
        try:
            item = yield define.req_msg_queue.get()
            client = item['client']
            msg = item['data']
            if isinstance(msg, str):
                msg = json.loads(msg)
            yield define.message_processor.process_message(client, msg)
            define.req_msg_queue.task_done()
        except:
            pass


@gen.coroutine
def process_res_loop():
    print('process res loop start')
    while True:
        try:
            item = yield define.res_msg_queue.get()
            client = item['client']
            if client and client.connected:
                client.write_message(json.dumps(item['data'], ensure_ascii=False))
            define.res_msg_queue.task_done()
        except:
            pass

