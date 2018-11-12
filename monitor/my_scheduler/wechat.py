# -*- coding: utf-8 -*-
from smtplib import SMTPException
from rauma.settings import *
from monitor.my_scheduler import email_send
from wxpy import *
import monitor.my_util.my_conf as my_conf

import logging

log = logging.getLogger(__name__)
bot = Bot(cache_path=True, console_qr=True)


# 心跳检测
def heart():
    try:
        group = bot.groups().search("account")[0]
        log.info("wechat heart success")
    except Exception as e:  # 如果请求失败
        message = "wechat heart error.err_msg:%s" % (e.message)
        email_send.send(my_conf.notify_email_subject, message,
                        my_conf.notify_email_manager.encode('unicode-escape').decode('string_escape').split(","))
        log.error(message)


# 发送微信
def send(group_name, msg):
    try:
        group = bot.groups().search(group_name)[0]
        group.send_msg(msg)
        log.info("send wechat success msg:%s to %s group" % (msg, group))
    except Exception as ex:
        print ("send wechat fail " + ex.message)
