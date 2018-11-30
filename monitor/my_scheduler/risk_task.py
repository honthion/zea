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
from monitor.my_util.serializers import *
from decimal import *
from monitor.models import *
from monitor.my_util.time_util import *

log = logging.getLogger(__name__)

# 通过率检查 来源于  queryUserTransferReportDetail
pass_rate_sql = "SELECT registerCount , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate,  IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate FROM ( SELECT DATE, SUM(clickCount) AS clickCount, SUM(applyCount) AS applyCount , SUM(registerCount) AS registerCount, SUM(applySuccessCount) AS applySuccessCount , SUM(orderCount) AS orderCount, SUM(orderMoney) AS orderMoney , IFNULL(CAST(applyCount / registerCount AS DECIMAL(8, 4)), 0) AS registerApplyRate , IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT IFNULL(SUM(clickCount), 0) AS clickCount, 0 AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(countDate) AS DATE FROM daoliu_platform_click WHERE 1 = 1 GROUP BY DATE(countDate) UNION ALL SELECT 0 AS clickCount, IFNULL(COUNT(1), 0) AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(registerTime) AS DATE FROM `user` WHERE 1 = 1 GROUP BY DATE(registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount , IFNULL(COUNT(1), 0) AS applyCount , 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE 1 = 1 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount , IFNULL(COUNT(1), 0) AS applySuccessCount , 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.state = 7 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount, 0 AS applySuccessCount , IFNULL(COUNT(DISTINCT userId), 0) AS orderCount , IFNULL(SUM(t1.primeCost), 0) AS orderMoney , DATE(t2.registerTime) AS DATE FROM credit_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.loanState = 3 GROUP BY DATE(t2.registerTime) ) b WHERE 1 = 1 GROUP BY b.date ) c ORDER BY c.date DESC LIMIT 10;  SELECT registerCount, IFNULL(CAST(applyCount / registerCount AS DECIMAL(8, 4)), 0) AS registerApplyRate , IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT DATE, SUM(clickCount) AS clickCount, SUM(applyCount) AS applyCount , SUM(registerCount) AS registerCount, SUM(applySuccessCount) AS applySuccessCount , SUM(orderCount) AS orderCount, SUM(orderMoney) AS orderMoney , IFNULL(CAST(applyCount / registerCount AS DECIMAL(8, 4)), 0) AS registerApplyRate , IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT IFNULL(SUM(clickCount), 0) AS clickCount, 0 AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(countDate) AS DATE FROM daoliu_platform_click WHERE 1 = 1 GROUP BY DATE(countDate) UNION ALL SELECT 0 AS clickCount, IFNULL(COUNT(1), 0) AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(registerTime) AS DATE FROM `user` WHERE 1 = 1 GROUP BY DATE(registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount , IFNULL(COUNT(1), 0) AS applyCount , 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE 1 = 1 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount , IFNULL(COUNT(1), 0) AS applySuccessCount , 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.state = 7 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount, 0 AS applySuccessCount , IFNULL(COUNT(DISTINCT userId), 0) AS orderCount , IFNULL(SUM(t1.primeCost), 0) AS orderMoney , DATE(t2.registerTime) AS DATE FROM credit_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.loanState = 3 GROUP BY DATE(t2.registerTime) ) b WHERE 1 = 1 GROUP BY b.date ) c ORDER BY c.date DESC LIMIT 1;"
# 失败原因检查 单项大于30%
fail_reason_sql = '''
                    
                   SELECT s1.failReason,  s1.failCount / s2.total AS rate
                   FROM
                     (SELECT t1.failReason, COUNT(0) AS failCount
                      FROM identificate_order t1
                      WHERE t1.failReason != ''  AND DATE(t1.failTime) >= CURDATE()
                      GROUP BY t1.failReason) s1,
                     (SELECT COUNT(0) AS total
                      FROM identificate_order t1
                      WHERE t1.failReason != '' AND DATE(t1.failTime) >= CURDATE() ) s2 
                    WHERE s1.failCount / s2.total > 0.3
                '''
# 借款率监控
pass_loan_rate_sql = '''
SELECT u1.`platformId` id,
       dp.`platformName` `name`,
       u1.rsc pc,
       IFNULL(u2.oc, 0) oc,
       IFNULL(u2.oc, 0)/u1.rsc rate
FROM
  (-- 认证成功量
SELECT COUNT(0) rsc,
       `platformId`
   FROM `user`
   WHERE DATE(`registerTime`)= "%s"
   AND (hasIdentified=1 OR loanCount>0)
   GROUP BY `platformId`
   HAVING rsc >=%d )u1
LEFT JOIN
  (-- 借款人数
SELECT COUNT(0) oc,
       u.`platformId`
   FROM `user` u
   LEFT JOIN credit_order co ON co.userId =u.id
   WHERE DATE(u.`registerTime`)= "%s"
     AND co.`loanState` = 3
   GROUP BY `platformId`) u2 ON u1.`platformId`=u2.`platformId`
LEFT JOIN `daoliu_platform` dp ON dp.id = u1.`platformId`
WHERE IFNULL(u2.oc, 0)/IFNULL(u1.rsc, 0)>=%f
ORDER BY rate DESC
'''

# 首逾-自然还款率
overdue_rate_m1_sql = '''SELECT r1.id,
       r1.name,
       r1.cnt,
       IFNULL(r2.cnt, 0) cnt2,
       IFNULL(r2.cnt, 0)/r1.cnt rate
FROM
  (SELECT dp.id,
          dp.`platformName` `name`,
          COUNT(0) cnt
   FROM `credit_order` co
   LEFT JOIN `user` u ON u.id = co.`userId`
   LEFT JOIN `daoliu_platform` dp ON dp.id = u.`platformId`
    WHERE DATEDIFF(co.`latestPaymentDate`,CURDATE()) = -1
   GROUP BY u.`platformId`
   HAVING cnt>=%d) r1
LEFT JOIN
  (SELECT u.`platformId` id,
          COUNT(0) cnt
   FROM `credit_order` co
   LEFT JOIN `user` u ON u.id = co.`userId`
   WHERE DATEDIFF(co.`latestPaymentDate`,CURDATE()) = -1
   AND  DATEDIFF(co.`paymentDate`,CURDATE()) <= -1
   GROUP BY u.`platformId`) r2 ON r1.id = r2.id
WHERE IFNULL(r2.cnt, 0)/r1.cnt <=%f
ORDER BY rate 
'''


# 通过率检查
def risk_pass_rate():
    task_success = False
    lv = 0
    db = None
    count = []
    item = ItemEnum.risk_pass_rate
    msg = ''
    date_msg = get_time_period(0)
    try:
        db = my_db.get_turku_db()
        if not db:
            db_task.db_error()
            log.error("get db error.")
            return
        cursor = db.cursor()
        cursor.execute(pass_rate_sql)
        # [注册量，注册放款率，申请成功率]
        count = cursor.fetchone()
        # 当日的注册数>50的情况下，注册放款率或者审核通过率=0，level=1；注册放款率<5%*或者审核通过率<10%, level=2
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        # if  count[0] > 50 and count[1] * count[2] != 0:
        if count[0] > 50 and count[1] * count[2] == 0:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1') % (count[1] * 100, count[2] * 100)))
        if count[1] < 0.05 or count[2] < 0.1:
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg1') % (count[1] * 100, count[2] * 100)))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error(
            "risk_pass_rate alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count, default=defaultencode), te.level, te.msg))
    except Exception as e:
        msg = "risk_pass_rate fail."
        log.error("risk_pass_rate fail.data:%s,msg:%s" % (json.dumps(count, default=defaultencode), e.message))
    finally:
        if db:
            db.close()
        record_save.save_record(item, lv, task_success, date_msg, msg)
        return count


# failReason异常检查
def fail_reason():
    task_success = False
    lv = 0
    db = None
    count = []
    item = ItemEnum.fail_reason
    msg = ''
    date_msg = get_time_period(0)
    try:
        db = my_db.get_turku_db()
        if not db:
            db_task.db_error()
            log.error("get db error.")
            return
        cursor = db.cursor()
        cursor.execute(fail_reason_sql)
        # [命中名称，今日占比]
        count = cursor.fetchall()
        # 该failreaon占比>50%，level=2
        if count:
            # if not count:
            lv = 2
            data = [item.value.get('msg1') % (c[0], c[1] * 100) for c in count]
            raise (TaskException(item, lv, "failReason异常\n" + "".join(data)))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error(
            "fail_reason alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count, default=defaultencode), te.level, te.msg))
    except Exception as e:
        msg = "fail_reason fail."
        log.error("fail_reason fail.data:%s,msg:%s" % (json.dumps(count, default=defaultencode), e.message))
    finally:
        if db:
            db.close()
        record_save.save_record(item, lv, task_success, date_msg, msg)
        return count


# 通过借款率监控
def pass_loan_rate():
    task_success = False
    lv = 0
    db = None
    count = []
    item = ItemEnum.pass_loan_rate
    msg = ''
    date_msg = get_time_period(0)
    try:
        db = my_db.get_turku_db()
        if not db:
            db_task.db_error()
            log.error("get db error.")
            return
        cursor = db.cursor()
        # 判断是否是凌晨
        zero_clock = abs(time_util.gettime(0) - time.time()) < 60
        # zero_clock = True
        date_str = get_delta_date(-1) if zero_clock else get_delta_date(0)
        sql = pass_loan_rate_sql % (date_str, 10, date_str, 0.9)
        date_msg = get_delta_date(-1) if zero_clock else get_time_period(0)
        cursor.execute(sql)
        # [id，平台名称，通过人数，首借人数，通过借款率]
        count = cursor.fetchall()
        count_new = []
        if count:
            # 找出所有的今天免预警的名称
            free_plf_names = Item.objects.filter(id=10)[0].free_data.split(",")
            for c in count:
                if c[1] not in free_plf_names:
                    count_new.append(c)

        # if not count_new:
        if count_new:
            lv = 2
            data = [item.value.get('msg1') % (c[1], c[4] * 100) for c in count_new]
            raise (TaskException(item, lv, "通过借款率\n" + "".join(data)))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error(
            "pass_loan_rate alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count, default=defaultencode), te.level, te.msg))
    except Exception as e:
        msg = "pass_loan_rate fail."
        log.error("pass_loan_rate fail.data:%s,msg:%s" % (json.dumps(count, default=defaultencode), e.message))
    finally:
        if db:
            db.close()

        record_save.save_record(item, lv, task_success, date_msg, msg)
        return count_new


# 渠道首逾监控
def overdue_rate_m1():
    task_success = False
    lv = 0
    db = None
    count = []
    item = ItemEnum.overdue_rate_m1
    msg = ''
    date_msg = get_delta_date(-1)
    try:
        db = my_db.get_turku_db()
        if not db:
            db_task.db_error()
            log.error("get db error.")
            return
        cursor = db.cursor()
        cursor.execute(overdue_rate_m1_sql % (8, 0.5))
        # [id，平台名称，应还笔数，自然还款笔数，自然还款率]
        count = cursor.fetchall()
        if count:
            # if not count:
            lv = 2
            data = [item.value.get('msg1') % (c[1], c[4] * 100) for c in count]
            raise (TaskException(item, lv, "自然还款率\n" + "".join(data)))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error(
            "overdue_rate_m1 alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count, default=defaultencode), te.level, te.msg))
    except Exception as e:
        msg = "overdue_rate_m1 fail."
        log.error("overdue_rate_m1 fail.data:%s,msg:%s" % (json.dumps(count, default=defaultencode), e.message))
    finally:
        if db:
            db.close()
        record_save.save_record(item, lv, task_success, date_msg, msg)
        return count
