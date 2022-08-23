#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import platform

system = platform.system().lower()


def convert_path(path):
    if system == 'windows':
        return path.lstrip('/').replace('/', '\\')
    else:
        return path.lstrip('/')
