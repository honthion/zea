# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import detail_route

from monitor.models import Item, Group, GroupItem, Record
from monitor.pojo.my_enum import *
from monitor.serializers import ItemSerializer, UserSerializer

log = logging.getLogger(__name__)


# 首页
@login_required(login_url='/login')
def index(request):
    return render(request, 'index.html')


# 欢迎页面
def welcome(request):
    return render(request, 'welcome.html')


# 登陆
def login_index(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            log.info("login account:%s" % (username))
            return render(request, 'index.html')
        else:
            log.error("disabled account:%s" % (username))
            return render(request, 'login.html', {'errmsg': 'disabled account'})
    else:
        log.error("invalid login:%s" % (username))
        return render(request, 'login.html', {'errmsg': 'invalid login'})


# 登出
def logout_view(request):
    logout(request)
    return render(request, 'login.html')


# 用户注册
def register(request):
    if request.method == 'GET':
        return HttpResponse('ok')
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(username=username, email=password, password=password)
    user.save()
    return HttpResponse('register succ')


# 获取监控大盘数据
@login_required(login_url='/login')
def index(request):
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


# 包含单个状态修改
@login_required(login_url='/login')
def recordSingle(request, record_id='0'):
    requestMethod = request.method
    print requestMethod
    try:
        if 'PUT' == requestMethod:
            if record_id != 0:
                record = Record.objects.get(id=record_id)
                requestBody = json.loads(request.body)
                record.remark = requestBody.get('remark')
                # 修改现有的
                record.save()
        elif 'GET' == requestMethod:
            # 需要获取 分组信息
            record = Record.objects.get(id=record_id)
            return render(request, 'monitor/monitor-record-edit.html', {'record': record})
        else:
            pass
    except Exception as e:
        print ("Exception!" + e.message)
        return JsonResponse({"success": False, "msg": e.message, "data": ""})
    return JsonResponse({"success": True, "msg": "", "data": ""})


def page_not_found(request):
    from django.shortcuts import render
    return render(request, '404.html')


# ---------------------------下面是接口---------------------------
from django.contrib.auth.models import User
from rest_framework.response import Response

# ---------------------------user
from rest_framework import viewsets


# class UserViewSet(mixins.CreateModelMixin,
#                                 mixins.ListModelMixin,
#                                 mixins.RetrieveModelMixin,
#                                 viewsets.GenericViewSet):
#     """
#     Example empty viewset demonstrating the standard
#     actions that will be handled by a router class.

#     If you're using format suffixes, make sure to also include
#     the `format=None` keyword argument for each action.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


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
