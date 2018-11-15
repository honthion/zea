# -*- coding: utf-8 -*-
import random
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging
import base_task, account_task, risk_task
from monitor.models import *
from monitor.pojo.my_enum import *
import monitor.my_util.my_db as my_db

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


# 账号登陆
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.base_task.value.get('mon_trigger')), replace_existing=True)
def account_login():
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=ItemEnum.base_task.value.get('mon_title'))
    if item and item[0].mon_status == 1:
        base_task.account_login()


# 当日注册
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.today_register.value.get('mon_trigger')),
              replace_existing=True)
def today_register():
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=ItemEnum.today_register.value.get('mon_title'))
    if item and item[0].mon_status == 1:
        account_task.today_register()


# 当日贷款
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.today_loan_amount.value.get('mon_trigger')),
              replace_existing=True)
def today_loan_amount():
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=ItemEnum.today_loan_amount.value.get('mon_title'))
    if item and item[0].mon_status == 1:
        account_task.today_loan_amount()


# 当日回款
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.today_repay.value.get('mon_trigger')), replace_existing=True)
def today_repay():
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=ItemEnum.today_repay.value.get('mon_title'))
    if item and item[0].mon_status == 1:
        account_task.today_repay()


# 还款短信和语音提醒
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.repayment_sms.value.get('mon_trigger')),
              replace_existing=True)
def repayment_sms():
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=ItemEnum.repayment_sms.value.get('mon_title'))
    if item and item[0].mon_status == 1:
        account_task.repayment_sms()


# 催收案件分配
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.collection_assign.value.get('mon_trigger')),
              replace_existing=True)
def collection_assign():
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=ItemEnum.collection_assign.value.get('mon_title'))
    if item and item[0].mon_status == 1:
        account_task.collection_assign()


# 账户余额
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.account_balance.value.get('mon_trigger')),
              replace_existing=True)
def account_balance():
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=ItemEnum.account_balance.value.get('mon_title'))
    if item and item[0].mon_status == 1:
        account_task.account_balance()


# 通过率检查
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.risk_pass_rate.value.get('mon_trigger')),
              replace_existing=True)
def risk_pass_rate():
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=ItemEnum.risk_pass_rate.value.get('mon_title'))
    if item and item[0].mon_status == 1:
        risk_task.risk_pass_rate()


# failReason异常检查
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.fail_reason.value.get('mon_trigger')),
              replace_existing=True)
def fail_reason():
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=ItemEnum.fail_reason.value.get('mon_title'))
    if item and item[0].mon_status == 1:
        risk_task.fail_reason()


register_events(scheduler)
scheduler.start()
