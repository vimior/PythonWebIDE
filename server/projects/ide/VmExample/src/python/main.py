#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>

import time
import random
from utils.calc import add, sub


if __name__ == '__main__':
    a = 99
    b = 25
    print('{} + {} = {}'.format(a, b, add(a, b)))
    print('{} - {} = {}'.format(a, b, sub(a, b)))

    ret = 0

    while True:
        a = ret
        b = random.randint(1, 100)
        ret += b
        print('{} + {} = {}'.format(a, b, ret))
        time.sleep(1)

