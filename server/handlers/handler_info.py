#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, Vinman, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.cub@gmail.com>


class HandlerInfo(object):
    def __init__(self, *args, **kwargs) -> None:
        self.subprograms = {}
    
    def set_subprogram(self, program_id, sub_t):
        self.stop_subprogram(program_id)
        self.subprograms[program_id] = sub_t
    
    def remove_subprogram(self, program_id):
        if program_id is None:
            self.stop_subprogram()
            self.subprograms.clear()
        elif program_id in self.subprograms:
            self.stop_subprogram(program_id)
            self.subprograms.pop(program_id, None)
    
    def start_subprogram(self, program_id):
        if program_id in self.subprograms:
            self.subprograms[program_id].start()
    
    def stop_subprogram(self, program_id):
        if program_id is None:
            for _, t in self.subprograms.items():
                t.stop()
            for _, t in self.subprograms.items():
                try:
                    t.join()
                except:
                    pass
        elif program_id in self.subprograms:
            try:
                t = self.subprograms.pop(program_id)
                t.stop()
                t.join()
            except:
                pass

