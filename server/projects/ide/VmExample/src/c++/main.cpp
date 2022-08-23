/*
# Software License Agreement (MIT License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>
*/

#include <stdio.h>
#include "utils.hpp"

int main(int argc, char *argv[]) {
  Utils util;
  int a = 100;
  int b = 36;
  printf("%d + %d = %d\n", util.add(a, b));
  printf("%d - %d = %d\n", util.sub(a, b));
  return 0;
}