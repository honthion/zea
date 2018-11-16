# -*- coding: utf-8 -*-
import time, datetime


# 获取整点时间的时间戳
def gettime(val):
    a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % val
    timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(timeArray))
