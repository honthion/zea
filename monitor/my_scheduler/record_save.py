# -*- coding: utf-8 -*-
from monitor.pojo.my_enum import *
from monitor.models import *
from django.core.exceptions import *
import logging
from monitor.my_scheduler import email_send, wechat
import monitor.my_util.my_conf as my_conf
import json
from django.db import connection

log = logging.getLogger(__name__)


# 保存记录到数据库
def save_record(item_enum, lv, task_success, err_info):
    # 根据类型Id 查询出最后一次任务的数据
    mon_id = item_enum.value.get("id")
    mon_title = item_enum.value.get("mon_title")
    mon_type = item_enum.value.get("mon_type")
    record = None
    try:
        record = Record.objects.filter(mon_id=mon_id).latest()
    except Record.DoesNotExist:  # 如果对象不存在
        log.info("save_record but DoesNotExist.mon_id:%d" % (mon_id))
    try:
        if record == None or record.mon_status == MonitorStatusEnum.normal or record.mon_status == MonitorStatusEnum.recovery:  # 如果前一条是成功的
            record = Record.objects.create(mon_id=mon_id, mon_title=mon_title,
                                           mon_status=MonitorStatusEnum.normal if task_success else MonitorStatusEnum.alarm,
                                           mon_level=lv,
                                           err_info=err_info,
                                           mon_type=mon_type
                                           )
        else:  # 前一条是失败的
            record.mon_status = MonitorStatusEnum.recovery if task_success else MonitorStatusEnum.alarm
            record.save()
        log.info("save_record success:%s" % mon_title)

        if record != None and record.mon_status == MonitorStatusEnum.alarm:
            # 如果此条是失败的，将执行消息推送
            send_message(item_enum, lv, task_success, err_info)
    except Exception as err:
        log.error("save_record error.item_enum:%s,task_success:%r,remark:%s,errmsg:%s" % (
            mon_title, task_success, err_info, err.message))


# 发送消息
def send_message(item_enum, lv, task_success, msg):
    if task_success:
        return
    # 只有失败才进行推行
    mon_id = item_enum.value.get("id")
    mon_title = item_enum.value.get("mon_title")
    mon_type = item_enum.value.get("mon_type")
    mon_type_name = MonitorTypeEnum.display(mon_type)
    # 获取微信发送
    wx_tag_id = ''
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT GROUP_CONCAT(g.`notify_wx_tags_id`) FROM `monitor_group` g LEFT JOIN `monitor_group_item` gi ON gi.`gro_id` = g.`id`  WHERE gi.`mon_id` = %d AND g.`gro_status`=1" % (
                mon_id))
        raw = cursor.fetchone()
        wx_tag_id = raw[0].encode('unicode-escape').decode('string_escape')
    except Exception as e:
        log.error("get sql fail.")
    # 发送微信
    if wx_tag_id:
        wechat.send_message(split_to_set(wx_tag_id), lv,
                            "MJB-监控预警</br>分类：%s</br>名称：%s</br>描述：%s" % (mon_type_name, mon_title, msg))


def split_comma_to_set(str):
    str_list = str.split()
    return [] if len(str_list) == 0 else list(set(str_list))


# 文本
def split_to_set(str):
    str_list = str.split(',')
    li = ([] if len(str_list) == 0 else list(set(str_list)))
    if '' in li:
        li.remove('')
    return li
