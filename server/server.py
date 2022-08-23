#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import os
import argparse
from tornado import ioloop
from tornado import web
from tornado import httpserver
from command.processor import RequestProcessor, ResponseProcessor
from handlers.ws_handler import WebSocketHandler
from handlers.vue_handler import VueHandler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=str, default='0.0.0.0', help='server listen address')
    parser.add_argument('--port', type=int, default=10086, help='server listen port')
    parser.add_argument('--num_processes', type=int, default=-1, help='fork process to support')
    args = parser.parse_args()

    template_path = os.path.join(os.path.dirname(__file__), '..', 'dist', 'templates')
    static_path = os.path.join(os.path.dirname(__file__), '..', 'dist', 'static')
    settings = {
        'template_path': template_path,
        'static_path': static_path,
    }
    handlers = [
        (r'/ws', WebSocketHandler),
        (r'^.*$', VueHandler),
    ]

    # app = web.Application(handlers, **settings, autoreload=True)
    app = web.Application(handlers, **settings)

    if args.num_processes >= 0:
        try:
            http_server = httpserver.HTTPServer(app)
            http_server.bind(args.port, args.address)
            http_server.start(num_processes=args.num_processes)
        except:
            app.listen(args.port, address=args.address)
    else:
        app.listen(args.port, address=args.address)
    print('server listen on {}:{}'.format(args.address, args.port))
    pid = os.getpid()
    ppid = os.getppid()
    print('server process pid: {}, ppid: {}'.format(pid, ppid))

    req_processor = RequestProcessor()
    res_processor = ResponseProcessor()
    main_ioloop = ioloop.IOLoop.current()
    main_ioloop.add_timeout(1, req_processor.loop)
    main_ioloop.add_timeout(1, res_processor.loop)
    main_ioloop.start()


if __name__ == '__main__':
    main()
