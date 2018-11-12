# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from enum import Enum, unique
from pojo import my_enum


# 监控项
class Item(models.Model):
    ctime = models.DateTimeField(auto_now_add=True, null=False)  # 创建时间
    utime = models.DateTimeField(auto_now=True, null=False)  # 修改时间
    mon_title = models.CharField(max_length=100, null=False, blank=False, unique=True)  # 名称
    mon_type = models.PositiveSmallIntegerField(null=False, choices=my_enum.MonitorTypeEnum.ENUM_CHOICES)  # 类型
    mon_trigger = models.CharField(max_length=100, null=False)  # 触发器
    mon_trigger_desc = models.CharField(max_length=255, default='', null=False)  # 触发器解释
    mon_desc = models.CharField(max_length=1024, default='', null=False, blank=True)  # 描述
    mon_status = models.PositiveSmallIntegerField(default=1, null=False)  # 状态

    def __str__(self):
        return self.mon_title

    class Meta:
        ordering = ('mon_type',)


# 监控分组
class Group(models.Model):
    ctime = models.DateTimeField(auto_now_add=True, null=False)  # 创建时间
    utime = models.DateTimeField(auto_now=True, null=False)  # 修改时间
    gro_name = models.CharField(max_length=100, null=False, blank=False, unique=True)  # 名称
    notify_phone_no = models.CharField(max_length=1024, default='', null=False)  # 需要通知的电话号码
    notify_email = models.CharField(max_length=1024, default='', null=False)  # 需要通知的电话号码
    notify_wechat = models.CharField(max_length=1024, default='', null=False)  # 需要通知的微信号
    gro_desc = models.CharField(max_length=1024, default='', null=False, blank=True)  # 描述
    gro_status = models.PositiveSmallIntegerField(default=1, null=False)  # 状态

    def __str__(self):
        return self.gro_name

    class Meta:
        ordering = ('ctime',)


# 监控分组-监控项中间表
class GroupItem(models.Model):
    ctime = models.DateTimeField(auto_now_add=True, null=False)  # 创建时间
    utime = models.DateTimeField(auto_now=True, null=False)  # 修改时间
    gro_id = models.PositiveIntegerField(null=False)  # 分组id
    mon_id = models.PositiveIntegerField(null=False)  # 监控项id

    def __str__(self):
        return self.gro_id

    class Meta:
        ordering = ('ctime',)
        db_table = 'monitor_group_item'


# 监控记录表
class Record(models.Model):
    ctime = models.DateTimeField(auto_now_add=True, null=False)  # 创建时间
    utime = models.DateTimeField(auto_now=True, null=False)  # 修改时间，最后更新时间
    mon_id = models.PositiveIntegerField(null=False)  # 监控项id
    mon_type = models.PositiveIntegerField(default=0, null=False)  # 监控项类型id
    mon_title = models.CharField(max_length=100, null=False, blank=False)  # 监控项名称
    mon_status = models.PositiveSmallIntegerField(default=1, null=False,
                                                  choices=my_enum.MonitorStatusEnum.ENUM_CHOICES)  # 当前状态
    mon_level = models.PositiveSmallIntegerField(default=0, null=False)  # 风险级别
    err_info = models.CharField(max_length=1024, default='', null=False, blank=True)  # 错误信息
    remark = models.CharField(max_length=1024, default='', null=False, blank=True)  # 备注
    operator = models.CharField(max_length=256, default='', null=False, blank=True)  # 备注

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('-utime',)
        get_latest_by = "utime"
