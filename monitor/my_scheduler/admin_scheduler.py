# -*- coding: utf-8 -*-
import random
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging
import base_task, account_task, risk_task, colloction_task
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
    if check_task_status(ItemEnum.base_task):
        base_task.account_login()


# 当日注册
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.today_register.value.get('mon_trigger')),
              replace_existing=True)
def today_register():
    if check_task_status(ItemEnum.today_register):
        account_task.today_register()


# 当日贷款
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.today_loan_amount.value.get('mon_trigger')),
              replace_existing=True)
def today_loan_amount():
    if check_task_status(ItemEnum.today_loan_amount):
        account_task.today_loan_amount()


# 当日回款
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.today_repay.value.get('mon_trigger')), replace_existing=True)
def today_repay():
    if check_task_status(ItemEnum.today_repay):
        account_task.today_repay()


# 还款短信和语音提醒
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.repayment_sms.value.get('mon_trigger')),
              replace_existing=True)
def repayment_sms():
    if check_task_status(ItemEnum.repayment_sms):
        account_task.repayment_sms()


# 催收案件分配
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.collection_assign.value.get('mon_trigger')),
              replace_existing=True)
def collection_assign():
    if check_task_status(ItemEnum.collection_assign):
        colloction_task.collection_assign()


# 账户余额
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.account_balance.value.get('mon_trigger')),
              replace_existing=True)
def account_balance():
    if check_task_status(ItemEnum.account_balance):
        account_task.account_balance()


# 通过率检查
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.risk_pass_rate.value.get('mon_trigger')),
              replace_existing=True)
def risk_pass_rate():
    if check_task_status(ItemEnum.risk_pass_rate):
        risk_task.risk_pass_rate()


# failReason异常检查
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.fail_reason.value.get('mon_trigger')),
              replace_existing=True)
def fail_reason():
    if check_task_status(ItemEnum.fail_reason):
        risk_task.fail_reason()


# 通过借款率监控
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.pass_loan_rate.value.get('mon_trigger')),
              replace_existing=True)
def pass_loan_rate():
    if check_task_status(ItemEnum.pass_loan_rate):
        count_new = risk_task.pass_loan_rate()
        msg = ",".join([c[1] for c in count_new])
        record = Record.objects.filter(mon_id=10).latest()
        record.err_info = msg
        record.save()


# 渠道首逾监控
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.overdue_rate_m1.value.get('mon_trigger')),
              replace_existing=True)
def overdue_rate_m1():
    if check_task_status(ItemEnum.overdue_rate_m1):
        risk_task.overdue_rate_m1()


# 催收案件分配
# @register_job(scheduler, CronTrigger.from_crontab("0/1 * * * *"), replace_existing=True)
@register_job(scheduler, CronTrigger.from_crontab(ItemEnum.collection_rate.value.get('mon_trigger')),
              replace_existing=True)
def collection_rate():
    if check_task_status(ItemEnum.collection_rate):
        colloction_task.collection_rate()


# 每日清空Item表中的free_data
@register_job(scheduler, CronTrigger.from_crontab("5 0 * * *"), replace_existing=True)
def clean_free_data():
    Item.objects.filter(id=10).update(free_data='', free_date='')


# 判断是否启动这个定时任务
def check_task_status(item_enum):
    my_db.close_old_connections()
    item = Item.objects.filter(mon_title=item_enum.value.get('mon_title'),
                               mon_status=1).exclude(free_date=datetime.datetime.today())
    return item


register_events(scheduler)
scheduler.start()
