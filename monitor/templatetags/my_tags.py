# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from monitor.pojo.my_enum import *

register = template.Library()


# 获取监控类型的名称
@register.filter
def get_mon_type_name(mon_type):
    return MonitorTypeEnum.display(mon_type)
