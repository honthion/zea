# -*- coding: utf-8 -*-
import random
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging
import base_task,wechat
from monitor.pojo.my_enum import *

log = logging.getLogger(__name__)

executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# @register_job(scheduler, "interval", seconds=5, replace_existing=True)
# def test_job():
#     time.sleep(random.randrange(1, 100, 1) / 100.)

# @register_job(scheduler, CronTrigger.from_crontab('0 0 0 */1 *'), replace_existing=True)
# def cron_test():
#     print (datetime.datetime.now())

# 微信心跳
@register_job(scheduler, CronTrigger.from_crontab('0/5 * * * *'), replace_existing=True)
def wechat_heart():
    wechat.heart()

# 账号登陆
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.base_task.value.get('mon_trigger')), replace_existing=True)
def account_login():
    base_task.account_login()


register_events(scheduler)
scheduler.start()
