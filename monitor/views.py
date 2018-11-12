# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from monitor.models import Item, Group, GroupItem, Record
from monitor.serializers import ItemSerializer
from django.db import connection, transaction
from datetime import datetime
from monitor.pojo.my_enum import *

import logging

log = logging.getLogger(__name__)


# 获取监控大盘数据
@login_required(login_url='/login')
def index(request):
    log.info("index")
    querySet = Record.objects.raw("SELECT a.* "
                                  "FROM `monitor_record` AS a, "
                                  "(SELECT `mon_id` , MAX(`utime`) AS utime "
                                  "FROM `monitor_record` GROUP BY `mon_id`) AS b "
                                  "WHERE a.`mon_id`=b.`mon_id` AND a.`utime`=b.`utime`"
                                  "order by  find_in_set(a.`mon_id`,'2,3,1')")
    MonitorTypeEnum.display(1)
    return render(request, 'monitor/monitor-index.html', {'items': querySet, 'mon_type': MonitorTypeEnum})


# 获取所有的监控项
@login_required(login_url='/login')
def items(request):
    querySet = Item.objects.all()
    return render(request, 'monitor/monitor-item-list.html', {'items': querySet})


# 包含单个状态修改
@login_required(login_url='/login')
def item(request, item_id='0'):
    if request.method == 'PUT':
        if item_id != 0:
            try:
                item = Item.objects.get(id=item_id)
                requestBody = json.loads(request.body)
                item.mon_status = requestBody.get('mon_status')
                item.save()
                return JsonResponse({"success": True, "msg": "", "data": ""})
            except Item.DoesNotExist:
                print ("DoesNotExist!")
    print ("Error request!")
    return JsonResponse({"success": False, "msg": "", "data": ""})


# 获取所有的分组项
@login_required(login_url='/login')
def groups(request):
    requestMethod = request.method
    print requestMethod
    try:
        if 'GET' == requestMethod:
            querySet = Group.objects.all()
            return render(request, 'monitor/monitor-group-list.html', {'groups': querySet})
        elif 'POST' == requestMethod:
            requestBody = json.loads(request.body)
            gro_status = requestBody.get('gro_status')
            gro_name = requestBody.get('gro_name')
            gro_desc = requestBody.get('gro_desc')
            gro_status = requestBody.get('gro_status')
            notify_phone_no = requestBody.get('notify_phone_no', "")
            notify_email = requestBody.get('notify_email', "")
            item_str = requestBody.get('item_str')
            # todo 值没有校验
            # 插入
            print gro_name
            print gro_desc
            print gro_status
            print notify_phone_no
            print notify_email
            group = Group.objects.create(gro_name=gro_name, gro_desc=gro_desc, gro_status=gro_status,
                                         notify_email=notify_email,
                                         notify_phone_no=notify_phone_no, ctime=datetime.now(), utime=datetime.now())
            # 批量插入中间表
            item_ids = item_str.split()
            gro_item_list = []
            for item_id in item_ids:
                gro_item_list.append(GroupItem(gro_id=group.id, item_id=item_id))
            GroupItem.objects.bulk_create(gro_item_list)
    except Exception as e:
        print ("Exception!" + e.message)
        return JsonResponse({"success": False, "msg": e.message, "data": ""})
    return JsonResponse({"success": True, "msg": "", "data": ""})


# 获取新增分组页
@login_required(login_url='/login')
def group(request):
    print (request.user.username)
    # 需要获取 所有监控项
    itemQuerySet = Item.objects.all()
    return render(request, 'monitor/monitor-group-edit.html', {'item_list': itemQuerySet})


# 包含单个状态修改
@login_required(login_url='/login')
def groupSingle(request, gro_id='0'):
    requestMethod = request.method
    print requestMethod
    try:
        if 'PUT' == requestMethod:
            if gro_id != 0:
                group = Group.objects.get(id=gro_id)
                requestBody = json.loads(request.body)
                group.gro_status = requestBody.get('gro_status')
                gro_name = requestBody.get('gro_name')
                gro_desc = requestBody.get('gro_desc')
                if gro_name != None and gro_name != '' and gro_desc != None and gro_desc != '':
                    group.gro_name = requestBody.get('gro_name')
                    group.gro_status = requestBody.get('gro_status')
                    group.notify_phone_no = requestBody.get('notify_phone_no')
                    group.notify_email = requestBody.get('notify_email')
                    # 获取item_ids
                    item_str = requestBody.get('item_str')
                    item_ids = item_str.split()
                    # 删除既有的item
                    GroupItem.objects.filter(gro_id=gro_id).delete()
                    # 新增现有的
                    gro_item_list = []
                    for item_id in item_ids:
                        gro_item_list.append(GroupItem(gro_id=gro_id, item_id=item_id))
                    GroupItem.objects.bulk_create(gro_item_list)
                # 修改现有的
                group.save()
        elif 'GET' == requestMethod:
            # 需要获取 所有监控项
            itemQuerySet = Item.objects.all()
            # 需要获取 分组信息
            group = Group.objects.get(id=gro_id)
            item_list = []
            item_set = set()
            # 获取中间表的itemId集合数据
            groItemSet = GroupItem.objects.filter(gro_id=gro_id)
            for gro_item in groItemSet:
                item_set.add(gro_item.item_id)
            for itemQuery in itemQuerySet:
                item_vo = ItemVo.get_item(itemQuery)
                if itemQuery.id in item_set:
                    item_vo.isSelect = True
                item_list.append(item_vo)
            return render(request, 'monitor/monitor-group-edit.html', {'item_list': item_list, "group": group})
        else:
            pass
    except Exception as e:
        print ("Exception!" + e.message)
        return JsonResponse({"success": False, "msg": e.message, "data": ""})
    return JsonResponse({"success": True, "msg": "", "data": ""})


# ---------------------------下面是接口---------------------------


class ItemVo(Item):

    def __init__(self):
        super(Item, self).__init__()
        self.isSelect = False

    @staticmethod
    def get_item(item):
        item_vo = ItemVo()
        item_vo.mon_title = item.mon_title
        item_vo.id = item.id
        return item_vo


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GroupItemViewSet(viewsets.ModelViewSet):
    queryset = GroupItem.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
