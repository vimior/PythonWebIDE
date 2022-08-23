#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

from tornado import web


class VueHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")
