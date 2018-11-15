# -*- coding: utf-8 -*-
from smtplib import SMTPException
from rauma.settings import *
from monitor.my_scheduler import email_send
from wxpy import *
import monitor.my_util.my_conf as my_conf
import urllib2
import logging
import redis
import requests
from django.shortcuts import render, HttpResponse
from django_redis import get_redis_connection
from django.core.cache import cache
import logging
import json

log = logging.getLogger(__name__)

wx_mjb_token_key = "sln:rauma:db:wx:token:%d"
wx_mjb_apply_info_key = "sln:rauma:db:wx:apply_info"
wx_mjb_tag_list_key = "sln:rauma:db:wx:label_list"


# 获取token并存放在redis中
def get_token(lv):
    # 先获取redis中的值
    conn = get_redis_connection("default")
    token_key = wx_mjb_token_key % lv
    token = conn.get(token_key)
    if token is not None and len(token) > 0:
        return token
    # 通过接口获取
    retry = 0
    while retry < 3:
        try:
            request_url = my_conf.wx_get_token_url + (
                    '?corpid=%s&corpsecret=%s' % (my_conf.wx_corpid, get_agent_info(lv)[1]))
            log.info("request_url:%s,lv:%d" % (request_url, lv))
            response_str = requests.get(request_url).text
            log.info("response_str:%s,lv:%d" % (response_str, lv))
            response_map = json.loads(response_str)
            token = response_map.get('access_token', '')
            errcode = response_map.get('errcode', '-1')
            if errcode == 0 and len(token) > 0:
                log.info("get token success,token:%s" % (token))
                # 保存至redis
                conn.set(token_key, token, 5000)
                return token
        except Exception as e:
            log.error("get token fail,lv:%d,retry:%d,msg:%s" % (lv, retry, e.message))
            retry = retry + 1
    log.error("get token fail.")


# 发送消息
def send_message(tagids, lv, msg):
    if not msg:
        log.error("msg is null")
        return
    work_dict = get_work_dict(tagids, lv, msg)
    if not work_dict:
        log.error("get_work_dict fail")
    request_url = my_conf.wx_send_msg_url + ('?access_token=%s' % (get_token(lv)))
    log.info("request_url:%s,data:%s" % (request_url, json.dumps(work_dict)))
    header = {
        'dataType': "json",
        'Content-Type': 'application/json',
    }
    retry = 0
    while retry < 3:
        try:
            # 大坑  https://blog.csdn.net/testcs_dn/article/details/79755451
            response = requests.post(url=request_url, data=json.dumps(work_dict), headers=header)
            log.info("send_message success.msg:%s,response:%s" % (msg, response.text))
            return
        except Exception as e:
            log.error("send_message fail,retry:%d,msg:%s" % (retry, e.message))
            retry = retry + 1


# 获取微信标签
def get_tag_list(lv):
    conn = get_redis_connection("default")
    tag_list = conn.get(wx_mjb_tag_list_key)
    if tag_list:
        log.info("get tag list success,tag_list:%s" % (tag_list))
        return json.loads(tag_list)
    return get_tag_list_async(lv)


# 获取微信标签-
def get_tag_list_async(lv):
    conn = get_redis_connection("default")
    retry = 0
    try:
        while retry < 3:
            request_url = my_conf.wx_get_label_list + ('?access_token=%s' % (get_token(lv)))
            log.info("request_url:%s" % (request_url))
            response_str = requests.get(request_url).text
            log.info("response_str:%s" % (response_str))
            response_map = json.loads(response_str)
            taglist = response_map.get('taglist', [])
            errcode = response_map.get('errcode', '-1')
            if errcode == 0 and taglist:
                tag_list = json.dumps(taglist)
                log.info("get tag list success,tag_list:%s" % (tag_list))
                # 保存至redis
                conn.set(wx_mjb_tag_list_key, tag_list, 60)
                return taglist
            retry = retry + 1
    except  Exception as e:
        log.error("get tag list fail,retry:%d,msg:%s" % (retry, e.message))


# 获取传递的dict
def get_work_dict(tagids, lv, msg):
    # apply_dict = get_apply_dict()
    # if not apply_dict:
    #     log.error("apply_dict is null")
    #     return None
    work_dict = {}
    content = {}
    content['content'] = msg
    try:
        work_dict['agentid'] = get_agent_info(lv)[0]
        work_dict['msgtype'] = u'text'
        work_dict['text'] = content
        work_dict['toparty'] = ''
        work_dict['safe'] = '0'
        # 格式要求竖线
        work_dict['totag'] = "|".join(tagids)
        work_dict['touser'] = ''
    except Exception as e:
        log.error("apply_dict fail" + e.message)
    log.info("apply_dict return" + json.dumps(work_dict))
    return work_dict


def get_agent_info(lv):
    if lv == 0:
        return [my_conf.wx_mjb_agentid_lv0, my_conf.wx_mjb_secret_lv0]
    elif lv == 1:
        return [my_conf.wx_mjb_agentid_lv1, my_conf.wx_mjb_secret_lv1]
    elif lv == 2:
        return [my_conf.wx_mjb_agentid_lv2, my_conf.wx_mjb_secret_lv2]
    else:
        return []


def get_apply_dict():
    apply_info = get_apply_info()
    if not apply_info:
        log.error("apply_info:%s" % (apply_info))
        return None
    apply_dict = {}
    apply_info_dict = json.loads(apply_info)
    apply_dict['agentId'] = apply_info_dict.get('agentId')

    # 获取tagId
    tagids = ['5']
    if tagids:
        apply_dict['totag'] = "|".join(tagids)

    try:
        allow_tags = apply_info_dict.get('allow_tags')
        if True:
            tagids = allow_tags.get('tagid')
            if tagids:
                apply_dict['totag'] = "|".join(tagids)
    except Exception as e:
        log.error("get toTag fail:%s" % (apply_info))

    # 获取toParty
    try:
        allow_partys = apply_info_dict.get('allow_partys')
        if allow_partys:
            partyids = allow_partys.get('partyid')
            if partyids:
                apply_dict['toparty'] = "|".join(partyids)
    except Exception as e:
        log.error("get toParty fail:%s" % (apply_info))
    # 获取toUser
    try:
        allow_userinfos = apply_info_dict.get('allow_userinfos')
        user_id = ''
        if allow_userinfos:
            users = allow_userinfos['user']
            # for user in users:
            #     user_id = "|" + user.get('userid')
            apply_dict['touser'] = user_id[1:]
    except Exception as e:
        log.error("get toUser fail:%s" % (apply_info))
    log.info("get_apply_dict return" + json.dumps(apply_dict))
    return apply_dict


# 获取标签
def get_apply_info():
    # 先获取redis中的值
    conn = get_redis_connection("default")
    apply_info = conn.get(wx_mjb_apply_info_key)
    if apply_info:
        log.info("get apply_info success,response_str:%s" % (apply_info))
        return apply_info
    # 通过接口获取
    retry = 0
    while retry < 3:
        try:
            request_url = my_conf.wx_apply_info_url + (
                    '?access_token=%s&agentid=%s' % (get_token(), my_conf.wx_mjb_agentid_lv1))
            log.info("request_url:%s" % (request_url))
            response_str = requests.get(request_url).text
            log.info("response_str:%s" % (response_str))
            response_map = json.loads(response_str)
            errmsg = response_map.get('errmsg', '')
            errcode = response_map.get('errcode', '-1')
            if errcode == 0 and errmsg == 'ok':
                log.info("get apply_info success,response_str:%s" % (response_str))
                # 保存至redis
                conn.set(wx_mjb_apply_info_key, response_str, 5000)
                return response_str
        except Exception as e:
            log.error("get apply_info fail,retry:%d,msg:%s" % (retry, e.message))
            retry = retry + 1
    log.error("get apply_info fail.")
    return None


pass

# log = logging.getLogger(__name__)
# bot = Bot(cache_path=True, console_qr=True)
#
# try:
#     group = bot.groups().search("account")[0]
#     log.info("wechat heart success")
# except Exception as e:  # 如果请求失败
#     message = "wechat heart error.err_msg:%s" % (e.message)
#     email_send.send(my_conf.notify_email_subject, message,
#                     my_conf.notify_email_manager.encode('unicode-escape').decode('string_escape').split(","))
#     log.error(message)
# log = logging.getLogger(__name__)
# bot = Bot(cache_path=True, console_qr=True)
#
# try:
#     group = bot.groups().search(group_name)[0]
#     group.send_msg(msg)
#     log.info("send wechat success msg:%s to %s group" % (msg, group))
# except Exception as ex:
#     print ("send wechat fail " + ex.message)
