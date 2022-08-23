/*
# Software License Agreement (MIT License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>
*/

#include <stdio.h>
#include "hello.h"

int main(int argc, char *argv[]) {
  int a = 100;
  int b = 36;
  printf("%d + %d = %d\n", add(a, b));
  printf("%d - %d = %d\n", sub(a, b));
  return 0;
}