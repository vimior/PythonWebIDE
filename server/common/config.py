
#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import os
import sys

class Config:
    PYTHON = sys.executable
    # PROJECTS = os.path.join(os.path.abspath('.'), 'projects')
    PROJECTS = os.path.join(os.path.dirname(__file__), '..', 'projects')
