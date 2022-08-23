#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import sys
import logging

# logger_fmt = '[%(levelname)s] %(asctime)s [%(pathname)s:%(lineno)d]: %(message)s'
logger_fmt = '[%(levelname)s] %(asctime)s [%(filename)s:%(lineno)d]: %(message)s'
logger_date_fmt = '%Y-%m-%d %H:%M:%S'
stream_handler_fmt = logger_fmt
stream_handler_date_fmt = logger_date_fmt
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(stream_handler_fmt, stream_handler_date_fmt))
logger = logging.Logger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
