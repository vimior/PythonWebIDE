#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

from .ide_cmd import IdeCmd


class Command(IdeCmd):
    def __init__(self):
        self.isBeart = False
        self.beart_clients = []
        super(Command, self).__init__()
