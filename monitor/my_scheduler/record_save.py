# -*- coding: utf-8 -*-
from monitor.pojo.my_enum import *
from monitor.models import *
from django.core.exceptions import *
import logging
from monitor.my_scheduler import email_send, wechat
import monitor.my_util.my_conf as my_conf

from django.db import connection

log = logging.getLogger(__name__)


# 保存记录到数据库
def save_record(item_enum, task_success, err_info):
    # 根据类型Id 查询出最后一次任务的数据
    mon_id = item_enum.value.get("id")
    mon_title = item_enum.value.get("mon_title")
    mon_type = item_enum.value.get("mon_type")
    err_info = '' if task_success else err_info
    record = None
    try:
        record = Record.objects.filter(mon_id=mon_id).latest()
    except Record.DoesNotExist:  # 如果对象不存在
        log.info("save_record but DoesNotExist.mon_id:%d" % (mon_id))
    try:
        if record == None or record.mon_status == MonitorStatusEnum.normal or record.mon_status == MonitorStatusEnum.recovery:  # 如果前一条是成功的
            Record.objects.create(mon_id=mon_id, mon_title=mon_title,
                                  mon_status=MonitorStatusEnum.normal if task_success else MonitorStatusEnum.alarm,
                                  err_info=err_info,
                                  mon_type=mon_type
                                  )

        else:  # 前一条是失败的
            record.mon_status = MonitorStatusEnum.recovery if task_success else MonitorStatusEnum.alarm
            record.save()
        log.info("save_record success")

        if record != None and record.mon_status == MonitorStatusEnum.alarm:
            # 如果此条是失败的，将执行消息推送
            send_message(item_enum, task_success, err_info)
    except Exception as err:
        log.error("save_record error.item_enum:%s,task_success:%r,remark:%s,errmsg:%s" % (
            mon_title, task_success, err_info, err.message))


# 发送消息
def send_message(item_enum, task_success, remark):
    if task_success:
        return
    # 只有失败才进行推行
    mon_id = item_enum.value.get("id")
    mon_title = item_enum.value.get("mon_title")
    notify_msg = ''
    # 查询需要发送的人

    if item_enum == ItemEnum.base_task:
        notify_msg = mon_title + "失败，level=1"

    # 获取email 和 电话号码
    cursor = connection.cursor()
    cursor.execute(
        " SELECT GROUP_CONCAT(g.`notify_email`),GROUP_CONCAT(g.`notify_phone_no`) "
        "FROM `monitor_group` g "
        "LEFT JOIN `monitor_group_item` gi ON gi.`gro_id` = g.`id`  "
        "WHERE gi.`mon_id` = %d AND g.`gro_status`=1" % (
            mon_id))
    raw = cursor.fetchone()
    email_str = raw[0].encode('unicode-escape').decode('string_escape')
    phone_str = raw[1].encode('unicode-escape').decode('string_escape')
    # todo 如果未空的话还需要判断
    email_list = split_comma_to_set(email_str)
    phone_list = split_comma_to_set(phone_str)
    # 发送邮件
    if len(email_list) > 0:
        email_send.send(my_conf.notify_email_subject, notify_msg,
                        email_list)
    # 发送微信
    wechat.send("account", notify_msg)


def split_comma_to_set(str):
    str_list = str.split()
    return [] if len(str_list) == 0 else list(set(str_list))
