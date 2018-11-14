# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from monitor.pojo.my_enum import *
import monitor.my_util.my_conf as my_conf

register = template.Library()


# 获取监控类型的名称
@register.filter
def get_mon_type_name(mon_type):
    return MonitorTypeEnum.display(mon_type)


# 获取baseurl
@register.filter
def get_base_url():
    return my_conf.base_url
