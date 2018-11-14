#!/usr/bin/env python
# encoding: utf-8
from monitor.pojo.my_enum import *


class TaskException(Exception):
    '''
    Custom exception types
    '''

    def __init__(self, itemEnum, level, msg):
        Exception.__init__(self, msg)
        self.itemEnum = itemEnum
        self.level = level
        self.msg = msg
