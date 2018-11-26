# -*- coding: utf-8 -*-
import time, datetime


# 获取整点时间的时间戳
def gettime(val):
    a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % val
    timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(timeArray))


# 获取整点时间的时间戳
def get_time_str(val):
    date = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % val
    return date.strptime("%Y-%m-%d %H:%M:%S")


# 获取当前时间
def get_date_time_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 获取当前时间
def get_time_now(now):
    if not now:
        now = datetime.datetime.now()
    return now.strftime("%H:%M")


# 获取日期
def get_delta_date(val):
    now = datetime.datetime.now()
    date = now + datetime.timedelta(days=val)
    return date.strftime("%Y-%m-%d")


# 获取时间段（前几个小时 ~ 现在）
def get_time_period(val):
    if val == 0:
        return get_delta_date(0) + "00:00~" + get_time_now(datetime.datetime.now())
    else:
        now = datetime.datetime.now()
        date = now + datetime.timedelta(hours=val)
        return get_delta_date(0) + get_time_now(date) + "~" + get_time_now(now)
