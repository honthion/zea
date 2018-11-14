# -*- coding: utf-8 -*-
import requests
import json
from monitor.my_util import my_conf
import record_save
from monitor.pojo.my_enum import *
import monitor.my_scheduler.db_task as db_task
import logging, datetime, time
import monitor.my_util.my_db as my_db
import monitor.my_util.time_util as time_util
from monitor.pojo.my_exception import *

log = logging.getLogger(__name__)


# 当日注册用户
def today_register():
    task_success = False
    lv = 0
    db = None
    count = []
    item = ItemEnum.today_register
    msg = ''
    try:
        db = my_db.get_turku_db()
        if not db:
            db_task.db_error()
            log.error("get db error.")
            return
        cursor = db.cursor()
        cursor.execute(
            "SELECT  COUNT(0)  "
            "FROM `user`"
            "WHERE `registerTime` > DATE_SUB(NOW(), INTERVAL 1 HOUR) "
            ""
            "UNION ALL "
            ""
            "SELECT  COUNT(0)  "
            "FROM `user`"
            "WHERE `registerTime` BETWEEN DATE(NOW())  AND  NOW() "
            ""
            "UNION ALL "
            ""
            "SELECT  COUNT(0) FROM `user`"
            "WHERE `registerTime` BETWEEN DATE(DATE_SUB(NOW(),INTERVAL 1 DAY))  AND  DATE_SUB(NOW(), INTERVAL 1 DAY);")
        count = [row[0] for row in cursor.fetchall()]
        # 如果每小时注册量=0, level=1; 注册量<昨天同比30%，level=2
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        if count[0] == 0:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1')))
        if count[1] and count[2] and count[1] < count[2] * 0.3:
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg2')))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error("today_register alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count), te.level, te.msg))
    except Exception as e:
        msg = "today_register fail."
        log.error("today_register fail.data:%s,msg:%s" % (json.dumps(count), e.message))
    finally:
        if db:
            db.close()
        record_save.save_record(item, lv, task_success, msg)
        return count


# 当日放款
def today_loan_amount():
    task_success = False
    lv = 0
    db = None
    count = []
    item = ItemEnum.today_loan_amount
    msg = ''
    try:
        db = my_db.get_turku_db()
        if not db:
            db_task.db_error()
            log.error("get db error.")
            return
        cursor = db.cursor()
        cursor.execute(
            "SELECT  SUM(`primeCost`) "
            "FROM `credit_order` "
            "WHERE `orderTime` > DATE(NOW())"
            ""
            "UNION "
            ""
            "SELECT  SUM(`primeCost`)"
            "FROM `credit_order` "
            "WHERE `orderTime` BETWEEN DATE(DATE_SUB(NOW(),INTERVAL 1 DAY))  AND  DATE_SUB(NOW(), INTERVAL 1 DAY);")
        count = [row[0] for row in cursor.fetchall()]
        # 如果放款量=0, level=1; 放款量<昨天同比50%，level=2
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        if count[0] == 0:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1')))
        if count[1] and count[0] < count[1] * 0.5:
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg2')))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error("today_loan_amount alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count), te.level, te.msg))
    except Exception as e:
        msg = "today_loan_amount fail."
        log.error("today_loan_amount fail.data:%s,msg:%s" % (json.dumps(count), e.message))
    finally:
        if db:
            db.close()
        record_save.save_record(item, lv, task_success, msg)
        return count


# 当日回款
def today_repay():
    task_success = False
    lv = 0
    db = None
    count = []
    item = ItemEnum.today_repay
    msg = ''
    try:
        db = my_db.get_turku_db()
        if not db:
            db_task.db_error()
            log.error("get db error.")
            return
        cursor = db.cursor()
        cursor.execute(
            "SELECT COUNT(`primeCost`) "
            "FROM `credit_order`"
            "WHERE DATE(`paymentDate`)=DATE(NOW()) AND `repaymentState`=1 "

            "UNION "

            "SELECT COUNT(`primeCost`)"
            "FROM `credit_order`"
            "WHERE  DATE(`latestPaymentDate`)=DATE(NOW()) "

            "UNION "

            "SELECT COUNT(`primeCost`)"
            "FROM `credit_order`"
            "WHERE  `paymentDate` BETWEEN DATE(DATE_SUB(NOW(),INTERVAL 1 DAY)) AND  DATE_SUB(NOW(), INTERVAL 1 DAY) AND `repaymentState`=1 "

            "UNION "

            "SELECT COUNT(`primeCost`)"
            "FROM `credit_order`"
            "WHERE  DATE(`latestPaymentDate`)= DATE(DATE_SUB(NOW(),INTERVAL 1 DAY)) ")
        count = [row[0] for row in cursor.fetchall()]
        # 今日还款数，今日应还款数，昨日同期还款数，昨日应还款数
        count = [0, 3, 1, 3]
        # 如果回款量=0, level=1; 回款率 < 昨天同比30%，level=2；当天23:00时的回款率<60%, level=2;
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        if count[0] == 0:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1')))
        if count[1] and count[3] and float(count[0]) / count[1] < float(count[2]) / count[3] * 0.3:
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg2')))
        # 如果当前时间与23点时间差值在600s（10分钟）范围内
        is23clock = abs(time_util.gettime(23) - time.time()) < 500
        if is23clock and float(count[0]) / count[1] < 0.6:
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg3')))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error("today_loan_amount alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count), te.level, te.msg))
    except Exception as e:
        msg = "today_loan_amount fail."
        log.error("today_loan_amount fail.data:%s,msg:%s" % (json.dumps(count), e.message))
    finally:
        if db:
            db.close()
        record_save.save_record(item, lv, task_success, msg)
        return count
