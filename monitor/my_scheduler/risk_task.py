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

# 来源于  queryUserTransferReportDetail
pass_rate_sql = "SELECT registerCount,  IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT DATE, SUM(clickCount) AS clickCount, SUM(applyCount) AS applyCount , SUM(registerCount) AS registerCount, SUM(applySuccessCount) AS applySuccessCount , SUM(orderCount) AS orderCount, SUM(orderMoney) AS orderMoney , IFNULL(CAST(applyCount / registerCount AS DECIMAL(8, 4)), 0) AS registerApplyRate , IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT IFNULL(SUM(clickCount), 0) AS clickCount, 0 AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(countDate) AS DATE FROM daoliu_platform_click WHERE 1 = 1 GROUP BY DATE(countDate) UNION ALL SELECT 0 AS clickCount, IFNULL(COUNT(1), 0) AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(registerTime) AS DATE FROM `user` WHERE 1 = 1 GROUP BY DATE(registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount , IFNULL(COUNT(1), 0) AS applyCount , 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE 1 = 1 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount , IFNULL(COUNT(1), 0) AS applySuccessCount , 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.state = 7 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount, 0 AS applySuccessCount , IFNULL(COUNT(DISTINCT userId), 0) AS orderCount , IFNULL(SUM(t1.primeCost), 0) AS orderMoney , DATE(t2.registerTime) AS DATE FROM credit_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.loanState = 3 GROUP BY DATE(t2.registerTime) ) b WHERE 1 = 1 GROUP BY b.date ) c ORDER BY c.date DESC LIMIT 10;  SELECT registerCount, IFNULL(CAST(applyCount / registerCount AS DECIMAL(8, 4)), 0) AS registerApplyRate , IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT DATE, SUM(clickCount) AS clickCount, SUM(applyCount) AS applyCount , SUM(registerCount) AS registerCount, SUM(applySuccessCount) AS applySuccessCount , SUM(orderCount) AS orderCount, SUM(orderMoney) AS orderMoney , IFNULL(CAST(applyCount / registerCount AS DECIMAL(8, 4)), 0) AS registerApplyRate , IFNULL(CAST(applySuccessCount / applyCount AS DECIMAL(8, 4)), 0) AS applySuccessRate , IFNULL(CAST(orderCount / registerCount AS DECIMAL(8, 4)), 0) AS registerOrderRate FROM ( SELECT IFNULL(SUM(clickCount), 0) AS clickCount, 0 AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(countDate) AS DATE FROM daoliu_platform_click WHERE 1 = 1 GROUP BY DATE(countDate) UNION ALL SELECT 0 AS clickCount, IFNULL(COUNT(1), 0) AS registerCount , 0 AS applyCount, 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney , DATE(registerTime) AS DATE FROM `user` WHERE 1 = 1 GROUP BY DATE(registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount , IFNULL(COUNT(1), 0) AS applyCount , 0 AS applySuccessCount, 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE 1 = 1 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount , IFNULL(COUNT(1), 0) AS applySuccessCount , 0 AS orderCount, 0 AS orderMoney, DATE(t2.registerTime) AS DATE FROM identificate_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.state = 7 GROUP BY DATE(t2.registerTime) UNION ALL SELECT 0 AS clickCount, 0 AS registerCount, 0 AS applyCount, 0 AS applySuccessCount , IFNULL(COUNT(DISTINCT userId), 0) AS orderCount , IFNULL(SUM(t1.primeCost), 0) AS orderMoney , DATE(t2.registerTime) AS DATE FROM credit_order t1 INNER JOIN `user` t2 ON t1.userId = t2.id WHERE t1.loanState = 3 GROUP BY DATE(t2.registerTime) ) b WHERE 1 = 1 GROUP BY b.date ) c ORDER BY c.date DESC LIMIT 1;"


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
        # [注册量，申请成功率，注册放款率]
        count = cursor.fetchone()
        # 如果每小时注册量=0, level=1; 注册量<昨天同比30%，level=2
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        if count[0] > 50 and count[1] * count[2] == 0:
            lv = 1
            raise (TaskException(item, lv, item.value.get('msg1') % (count[1], count[2])))
        if count[1] < 0.1 or count[2] < 0.05:
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
