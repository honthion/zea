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
def get_base_url(a):
    return my_conf.base_url + str(a) if a != '0' else my_conf.base_url


#
# 分割平台名称
@register.filter
def split_plf_name(plf_names):
    if not plf_names:
        return u'<td class="td-status"><span class="radius">正常</span></td>'
    else:
        names = plf_names.split(',')
        s = u'<td class="td-status">'
        for name in names:
            s = s + u' <span class="radius btn btn-danger" title="点击关闭该项今日预警" onclick="monitor_record_status_plf(this,10,\'' + name + '\')">' + name + '</span>'
        s = s + ' </td>'
        return s
