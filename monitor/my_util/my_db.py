# -*- coding: utf-8 -*-
import MySQLdb
from django.db import connections
import monitor.my_util.my_conf as mc
import logging

log = logging.getLogger(__name__)

msg_data_not_exist = "无法获取数据"


# 获取turku 数据连接
def get_turku_db():
    db = None
    try:
        db = MySQLdb.connect(host=mc.turku_mysql_host,  # your host, usually localhost
                             port=mc.turku_mysql_port,
                             user=mc.turku_mysql_username,  # your username
                             passwd=mc.turku_mysql_password,  # your password
                             db=mc.turku_mysql_dbname)  # name of the data base
    except Exception as e:
        log.error("get db error.msg:%s" % e.message)
    return db


# 获取lasvegas 数据连接
def get_lasvegas_db():
    db = None
    try:
        db = MySQLdb.connect(host=mc.rmb_mysql_host,  # your host, usually localhost
                             port=mc.rmb_mysql_port,
                             user=mc.rmb_mysql_username,  # your username
                             passwd=mc.rmb_mysql_password,  # your password
                             db=mc.rmb_mysql_dbname)  # name of the data base
    except Exception as e:
        log.error("get db error.msg:%s" % e.message)
    return db


# https://blog.csdn.net/little_stupid_child/article/details/81774194  OperationalError: (2006, 'MySQL server has gone away')
def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()
