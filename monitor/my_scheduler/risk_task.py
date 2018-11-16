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

# 通过率检查 来源于  queryUserTransferReportDetail
pass_rate_sql = "SELECT registerCount , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate,  IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate FROM ( SELECT DATE, SUM(clickCount) AS clickCount, SUM(applyCount) AS applyCount , SUM(registerCount) AS registerCount, SUM(applySuccessCount) AS applySuccessCount , SUM(orderCount) AS orderCount, SUM(orderMoney) AS orderMoney , IFNULL(CAST(applyCount / registerCount AS DECIMAL(8, 4)), 0) AS registerApplyRate , IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT IFNULL(SUM(clickCount), 0) AS clickCount, 0 AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(countDate) AS DATE FROM daoliu_platform_click WHERE 1 = 1 GROUP BY DATE(countDate) UNION ALL SELECT 0 AS clickCount, IFNULL(COUNT(1), 0) AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(registerTime) AS DATE FROM `user` WHERE 1 = 1 GROUP BY DATE(registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount , IFNULL(COUNT(1), 0) AS applyCount , 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE 1 = 1 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount , IFNULL(COUNT(1), 0) AS applySuccessCount , 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.state = 7 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount, 0 AS applySuccessCount , IFNULL(COUNT(DISTINCT userId), 0) AS orderCount , IFNULL(SUM(t1.primeCost), 0) AS orderMoney , DATE(t2.registerTime) AS DATE FROM credit_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.loanState = 3 GROUP BY DATE(t2.registerTime) ) b WHERE 1 = 1 GROUP BY b.date ) c ORDER BY c.date DESC LIMIT 10;  SELECT registerCount, IFNULL(CAST(applyCount / registerCount AS DECIMAL(8, 4)), 0) AS registerApplyRate , IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT DATE, SUM(clickCount) AS clickCount, SUM(applyCount) AS applyCount , SUM(registerCount) AS registerCount, SUM(applySuccessCount) AS applySuccessCount , SUM(orderCount) AS orderCount, SUM(orderMoney) AS orderMoney , IFNULL(CAST(applyCount / registerCount AS DECIMAL(8, 4)), 0) AS registerApplyRate , IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT IFNULL(SUM(clickCount), 0) AS clickCount, 0 AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(countDate) AS DATE FROM daoliu_platform_click WHERE 1 = 1 GROUP BY DATE(countDate) UNION ALL SELECT 0 AS clickCount, IFNULL(COUNT(1), 0) AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(registerTime) AS DATE FROM `user` WHERE 1 = 1 GROUP BY DATE(registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount , IFNULL(COUNT(1), 0) AS applyCount , 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE 1 = 1 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount , IFNULL(COUNT(1), 0) AS applySuccessCount , 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.state = 7 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount, 0 AS applySuccessCount , IFNULL(COUNT(DISTINCT userId), 0) AS orderCount , IFNULL(SUM(t1.primeCost), 0) AS orderMoney , DATE(t2.registerTime) AS DATE FROM credit_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.loanState = 3 GROUP BY DATE(t2.registerTime) ) b WHERE 1 = 1 GROUP BY b.date ) c ORDER BY c.date DESC LIMIT 1;"
# 失败原因检查
fail_reason_sql = "SELECT s3.failReason, s3.rate, c3.rate, s3.rate / c3.rate FROM ( SELECT s1.failReason, s1.failCount, s1.failCount / s2.total AS rate FROM ( SELECT t1.failReason, COUNT(*) AS failCount FROM identificate_order t1 WHERE t1.failReason != '' AND DATE(t1.failTime) >= DATE(NOW()) GROUP BY t1.failReason ) s1, ( SELECT COUNT(0) AS total FROM identificate_order t1 WHERE t1.failReason != '' AND DATE(t1.failTime) >= DATE(NOW()) ) s2 ) s3 LEFT JOIN ( SELECT c1.failReason, c1.failCount, c1.failCount / c2.total AS rate FROM ( SELECT t1.failReason, COUNT(*) AS failCount FROM identificate_order t1 WHERE t1.failReason != '' AND (DATE(t1.failTime) BETWEEN DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) AND DATE_SUB(NOW(), INTERVAL 1 DAY) OR DATE(t1.failTime) BETWEEN DATE(DATE_SUB(NOW(), INTERVAL 2 DAY)) AND DATE_SUB(NOW(), INTERVAL 2 DAY) OR DATE(t1.failTime) BETWEEN DATE(DATE_SUB(NOW(), INTERVAL 3 DAY)) AND DATE_SUB(NOW(), INTERVAL 3 DAY)) GROUP BY t1.failReason ) c1, ( SELECT COUNT(0) AS total FROM identificate_order t1 WHERE t1.failReason != '' AND (DATE(t1.failTime) BETWEEN DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) AND DATE_SUB(NOW(), INTERVAL 1 DAY) OR DATE(t1.failTime) BETWEEN DATE(DATE_SUB(NOW(), INTERVAL 2 DAY)) AND DATE_SUB(NOW(), INTERVAL 2 DAY) OR DATE(t1.failTime) BETWEEN DATE(DATE_SUB(NOW(), INTERVAL 3 DAY)) AND DATE_SUB(NOW(), INTERVAL 3 DAY)) ) c2 ) c3 ON c3.failReason = s3.failReason WHERE s3.failCount > 10 AND s3.rate / c3.rate NOT BETWEEN 0.5 AND 1.5"


# 通过率检查
def risk_pass_rate():
    task_success = False
    lv = 0
    db = None
    count = []
    item = ItemEnum.risk_pass_rate
    msg = ''
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
        if count[0] > 50 and count[1] * count[2] == 0:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1') % (count[1], count[2])))
        if count[1] < 0.05 or count[2] < 0.1:
            lv = 2
            raise (TaskException(item, lv, item.value.get('msg2') % (count[1], count[2])))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error("risk_pass_rate alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count), te.level, te.msg))
    except Exception as e:
        msg = "risk_pass_rate fail."
        log.error("risk_pass_rate fail.data:%s,msg:%s" % (json.dumps(count), e.message))
    finally:
        if db:
            db.close()
        record_save.save_record(item, lv, task_success, msg)
        return count


# failReason异常检查
def fail_reason():
    task_success = False
    lv = 0
    db = None
    count = []
    item = ItemEnum.fail_reason
    msg = ''
    try:
        db = my_db.get_turku_db()
        if not db:
            db_task.db_error()
            log.error("get db error.")
            return
        cursor = db.cursor()
        cursor.execute(fail_reason_sql)
        # [命中名称，今日占比，过去三天占比，变化率]
        count = cursor.fetchall()
        # 每个failreason的数量>10的情况下，该failreaon占比比前3天同期的变化率>50%，level=2
        if count:
            lv = 2
            data = [item.value.get('msg1') % (c[0], c[3]) for c in count]
            raise (TaskException(item, lv,   ",".join(data)))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error("fail_reason alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count), te.level, te.msg))
    except Exception as e:
        msg = "fail_reason fail."
        log.error("fail_reason fail.data:%s,msg:%s" % (json.dumps(count), e.message))
    finally:
        if db:
            db.close()
        record_save.save_record(item, lv, task_success, msg)
        return count
