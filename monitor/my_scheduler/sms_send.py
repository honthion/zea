# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from smtplib import SMTPException
from rauma.settings import *
import logging

log = logging.getLogger(__name__)


# 发送短信
def send(subject, message, recipient_list):
    try:
        send_mail(
            subject=subject, message=message,
            from_email=EMAIL_HOST_USER, recipient_list=recipient_list, fail_silently=False,
        )
        log.info("send sms success.subject:%s,message:%s,recipient_list:[%s]" % (
            subject, message, ",".join(recipient_list)))
    except SMTPException as e:
        log.error("send sms error.subject:%s,message:%s,recipient_list:[%s],errmsg:%s" % (
            subject, message, ",".join(recipient_list), e.message))
