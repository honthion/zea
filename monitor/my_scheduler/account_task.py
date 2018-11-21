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
from decimal import Decimal as D
from monitor.my_util.serializers import *

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
        # [每小时注册量，今日注册量，昨日同期注册量]
        count = [row[0] for row in cursor.fetchall()]
        # 如果每小时注册量=0, level=1; 注册量<昨天同比30%，level=2
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        if count[0] == 0:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1')))
        if count[1] and count[2] and count[1] < count[2] * D(0.3):
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg2') % (count[1], count[2])))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error(
            "today_register alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count, default=defaultencode), te.level, te.msg))
    except Exception as e:
        msg = "today_register fail."
        log.error("today_register fail.data:%s,msg:%s" % (json.dumps(count, default=defaultencode), e.message))
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
            "WHERE `orderTime` > CURDATE()"
            ""
            "UNION "
            ""
            "SELECT  SUM(`primeCost`)"
            "FROM `credit_order` "
            "WHERE `orderTime` BETWEEN DATE(DATE_SUB(NOW(),INTERVAL 1 DAY))  AND  DATE_SUB(NOW(), INTERVAL 1 DAY);")
        # [今日放款量，昨日同期放款量]
        count = [row[0] for row in cursor.fetchall()]
        # 如果放款量=0, level=1; 放款量<昨天同比50%，level=2
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        if count[0] == 0:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1')))
        if count[1] and count[0] < count[1] * 0.5:
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg2') % (count[0], count[1])))
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
        cursor.execute('''
                    SELECT COUNT(0) 
                    FROM `credit_order`
                    WHERE   DATE(`latestPaymentDate`)=CURDATE()  AND `repaymentState`=1 
                    
                    UNION 
                    
                    SELECT COUNT(0)
                    FROM `credit_order`
                    WHERE  DATE(`latestPaymentDate`)=CURDATE() 
                    
                    UNION         
        
                    SELECT 
                    ( SELECT COUNT(0) 
                        FROM `credit_order` 
                        WHERE `paymentDate` <=  DATE_SUB(NOW(), INTERVAL 1 DAY)
                        AND `repaymentState` = 1 
                        AND  DATE(`latestPaymentDate`) = CURDATE() -1)
                        /
                       ( SELECT COUNT(0)
                        FROM `credit_order` 
                        WHERE DATE(`latestPaymentDate`) = CURDATE() -1)
        ''')
        # [今日还款数，今日应还款数，昨日还款率]
        count = [row[0] for row in cursor.fetchall()]
        # 如果回款量=0, level=1; 回款率 < 昨天同比30%，level=2；当天23:00时的回款率<60%, level=2;
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        if count[0] == 0:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1')))
        today = count[0] / count[1]
        if today < count[2] * D(0.3):
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg2') % (today * 100, count[2] * 100)))
        # 如果当前时间与23点时间差值在600s（10分钟）范围内
        is23clock = abs(time_util.gettime(23) - time.time()) < 600
        if is23clock and today < 0.6:
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg3') % today * 100))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error(
            "today_repay alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count, default=defaultencode), te.level, te.msg))
    except Exception as e:
        msg = "today_repay fail."
        log.error("today_repay fail.data:%s,msg:%s" % (json.dumps(count, default=defaultencode), e.message))
    finally:
        if db:
            db.close()
        record_save.save_record(item, lv, task_success, msg)
        return count


# 还款短信和语音提醒
def repayment_sms():
    task_success = False
    lv = 0
    db_lasvegas = None
    db_turku = None
    count_sms = []
    count_turku = []
    item = ItemEnum.repayment_sms
    msg = ''
    try:
        db_lasvegas = my_db.get_lasvegas_db()
        db_turku = my_db.get_turku_db()
        if not (db_lasvegas and db_turku):
            db_task.db_error()
            log.error("get db error.")
            return
        # 短信发送
        cursor_lasvegas = db_lasvegas.cursor()
        cursor_lasvegas.execute('''
            SELECT COUNT(0)  
            FROM `sms_send_log`  
            WHERE `deliver_status`=0 AND  `deliver_time` > CURDATE() AND `msg` REGEXP '^秒借呗.*您本期订单.*请知悉，谢谢！$' 
            ''')
        # [短信发送条数]
        count_sms = cursor_lasvegas.fetchone()
        # 语音发送
        cursor_turku = db_turku.cursor()
        cursor_turku.execute('''
        
        SELECT COUNT(0) 
        FROM `record_phone_no_operation` 
        WHERE DATE(ctime) = CURDATE() AND  `operation_type`=1 AND `operation_status`=1
        
        UNION ALL
        
        SELECT COUNT(0) 
        FROM `record_phone_no_operation` 
        WHERE DATE(ctime) = CURDATE()  AND  `operation_type`=1 AND `operation_status`=1 AND `remark` NOT BETWEEN 5 AND 6 
        
        UNION ALL
        
        SELECT COUNT(0) 
        FROM credit_order 
        WHERE loanState=3 AND repaymentState=0 
        AND (DATE(latestPaymentDate - 1)=CURDATE() OR DATE(latestPaymentDate)=CURDATE() )
        ''')
        count_turku = [row[0] for row in cursor_turku.fetchall()]
        # [语音发送条数,语音发送成功数，总短信发送条数]
        if not (count_sms and count_turku):
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        #  发送的成功率
        is_am = time_util.gettime(12) - time.time() > 0
        sms_success = float(count_sms[0]) / count_turku[2] > 0.8
        aida_success = count_turku[0] != 0 and float(count_turku[1]) / count_turku[0] > 0.2
        # 上午 判断 T，T-1 发送 成功功率小于80%
        if is_am and not sms_success and count_turku[0]:
            lv = 2
            msg = item.value.get('msg1') % (
                (count_turku[2], count_sms[0], float(count_sms[0]) / count_turku[2] * 100))
        # 下午 判断艾达语音 发送 成功功率小于20%
        if not is_am and not aida_success and count_turku[0]:
            lv = 2
            msg = item.value.get('msg2') % (
                (count_turku[0], count_turku[1],  float(count_turku[1]) / count_turku[0] * 100))
        if lv != 0:
            raise (TaskException(item, lv, msg))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error("repayment_sms  alarm.count_sms:%s,count_voice:%s,lv:%d,msg:%s" % (
            json.dumps(count_sms), json.dumps(count_turku), te.level, te.msg))
    except Exception as e:
        msg = "repayment_sms fail."
        log.error("repayment_sms fail.count_sms:%s,count_voice:%s,msg:%s" % (
            json.dumps(count_sms), json.dumps(count_turku), e.message))
    finally:
        if db_lasvegas:
            db_lasvegas.close()
        if db_turku:
            db_turku.close()
        record_save.save_record(item, lv, task_success, msg)
        return count_turku


# 催收案件分配
def collection_assign():
    task_success = False
    lv = 0
    db_turku = None
    count = []
    item = ItemEnum.collection_assign
    msg = ''
    try:
        db_turku = my_db.get_turku_db()
        if not db_turku:
            db_task.db_error()
            log.error("get db error.")
            return
        # 催收案件分配
        cursor_turku = db_turku.cursor()
        cursor_turku.execute(
            '''
            SELECT COUNT(0)
            FROM
              (SELECT DISTINCT `name`
               FROM manager
               WHERE `type` IN (5,
                                10,
                                12)
                 AND enabled = 1
                 AND `name` NOT IN
                   (SELECT DISTINCT `managerName`
                    FROM `urge_order`
                    WHERE DATE(outAddTime) = CURDATE())) s     
            '''
        )
        # [催收案件条数]
        count = cursor_turku.fetchone()
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        if count[0] != 0:
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg1')))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error("collection_assign alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count), te.level, te.msg))
    except Exception as e:
        msg = "collection_assign fail."
        log.error("collection_assign fail.data:%s,msg:%s" % (json.dumps(count), e.message))
    finally:
        if db_turku:
            db_turku.close()
        record_save.save_record(item, lv, task_success, msg)
        return count


# 账户余额
def account_balance():
    task_success = False
    lv = 0
    db_turku = None
    count = []
    item = ItemEnum.account_balance
    msg = ''
    try:
        db_turku = my_db.get_turku_db()
        if not db_turku:
            db_task.db_error()
            log.error("get db error.")
            return
        cursor_turku = db_turku.cursor()
        # 昨天同期下2个小时放款量的1.5倍
        cursor_turku.execute(
            "SELECT  SUM(`primeCost`) "
            "FROM `credit_order` "
            "WHERE `orderTime` BETWEEN DATE_SUB(NOW(),INTERVAL 24 HOUR)  AND  DATE_SUB(NOW(), INTERVAL 22 HOUR); ")
        # [昨天同期下2个小时放款量]
        count = cursor_turku.fetchone()
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        # 获取账户余额
        request_url = my_conf.yibao_account_balance
        log.info("request_url:%s" % (request_url))
        response_str = requests.get(request_url).text
        log.info("response_str:%s" % (response_str))
        response_map = json.loads(response_str)
        valid_amount = float(response_map.get('validAmount', '-1'))
        if valid_amount and valid_amount < count[0] * 1.5:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1') % (valid_amount, count[0])))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error("account_balance alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count), te.level, te.msg))
    except Exception as e:
        msg = "account_balance fail."
        log.error("account_balance fail.data:%s,msg:%s" % (json.dumps(count), e.message))
    finally:
        if db_turku:
            db_turku.close()
        record_save.save_record(item, lv, task_success, msg)
        return count
