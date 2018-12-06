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
from monitor.my_util.time_util import *

log = logging.getLogger(__name__)
# 催收状态
# stage	说明	    urgeOrderState	managerType
# S1	逾期1-3天	0	5
# S2	逾期4-9天	12	10
# S2P	逾期10-15天	14	17
# S3	逾期16-30天	13	12
# M2	逾期31-60天	2	19
# Bad	逾期60+天	3

sql_collection_rate = '''
        
select CONCAT(u1.le,'|',m.name) `name`,u1.dd,u1.cnt1,u1.cnt0 FROM(
-- S1
select 'S1' `le`, s0.managerId,s0.cnt1,CONCAT('催回率:',TRUNCATE(IFNULL(s1.cnt2,0)/s0.cnt1 * 100,2),'%') cnt0,CONCAT(SUBDATE(CURDATE(),INTERVAL 3 DAY),' ~ ',SUBDATE(CURDATE(),INTERVAL 1 DAY)) dd
FROM (
select managerId,count(0) cnt1
from turku.urge_order_log t1
where state=0 AND time BETWEEN SUBDATE(CURDATE(),INTERVAL 3 DAY) AND CURDATE()
group by managerId HAVING cnt1> 30)s0
LEFT JOIN (
select  t1.managerId,count(0) cnt2
from turku.urge_order_log t1
left JOIN turku.urge_order x1 
on t1.orderId = x1.orderId
where t1.state=0 AND t1.time BETWEEN SUBDATE(CURDATE(),INTERVAL 3 DAY) AND CURDATE()
and  x1.paymentDate IS NOT NULL AND x1.state = 0
GROUP BY t1.managerId)s1 on s0.managerId= s1.managerId
where IFNULL(s1.cnt2,0)/s0.cnt1 < 0.58
-- S2
UNION ALL
select 'S2' `le`, s0.managerId,s0.cnt1,CONCAT('催回单量:',IFNULL(s1.cnt2,0)) cnt0,CONCAT(SUBDATE(CURDATE(),INTERVAL 3 DAY),' ~ ',SUBDATE(CURDATE(),INTERVAL 1 DAY)) dd
FROM (
select managerId,count(0) cnt1
from turku.urge_order_log t1
where state=12 AND time BETWEEN SUBDATE(CURDATE(),INTERVAL 3 DAY) AND CURDATE()
group by managerId HAVING cnt1> 30)s0
LEFT JOIN (
select  t1.managerId,count(0) cnt2
from turku.urge_order_log t1
left JOIN turku.urge_order x1 
on t1.orderId = x1.orderId
where t1.state=12 AND t1.time BETWEEN SUBDATE(CURDATE(),INTERVAL 3 DAY) AND CURDATE()
and  x1.paymentDate IS NOT NULL AND x1.state = 12
GROUP BY t1.managerId)s1 on s0.managerId= s1.managerId
where IFNULL(s1.cnt2,0) < 3
-- S3P
UNION ALL
select 'S2P' `le`, s0.managerId,s0.cnt1,CONCAT('催回单量:',IFNULL(s1.cnt2,0)) cnt0,CONCAT(SUBDATE(CURDATE(),INTERVAL 5 DAY),' ~ ',SUBDATE(CURDATE(),INTERVAL 1 DAY)) dd
FROM (
select managerId,count(0) cnt1
from turku.urge_order_log t1
where state=14 AND time BETWEEN SUBDATE(CURDATE(),INTERVAL 5 DAY) AND CURDATE()
group by managerId HAVING cnt1> 30)s0
LEFT JOIN (
select  t1.managerId,count(0) cnt2
from turku.urge_order_log t1
left JOIN turku.urge_order x1 
on t1.orderId = x1.orderId
where t1.state=14 AND t1.time BETWEEN SUBDATE(CURDATE(),INTERVAL 5 DAY) AND CURDATE()
and  x1.paymentDate IS NOT NULL AND x1.state = 14
GROUP BY t1.managerId)s1 on s0.managerId= s1.managerId
where IFNULL(s1.cnt2,0) < 2
-- S3
UNION ALL
select 'S3' `le`, s0.managerId,s0.cnt1,CONCAT('催回单量:',IFNULL(s1.cnt2,0)) cnt0,CONCAT(SUBDATE(CURDATE(),INTERVAL 10 DAY),' ~ ',SUBDATE(CURDATE(),INTERVAL 1 DAY)) dd
FROM (
select managerId,count(0) cnt1
from turku.urge_order_log t1
where state=13 AND time BETWEEN SUBDATE(CURDATE(),INTERVAL 10 DAY) AND CURDATE()
group by managerId HAVING cnt1> 30)s0
LEFT JOIN (
select  t1.managerId,count(0) cnt2
from turku.urge_order_log t1
left JOIN turku.urge_order x1 
on t1.orderId = x1.orderId
where t1.state=13 AND t1.time BETWEEN SUBDATE(CURDATE(),INTERVAL 10 DAY) AND CURDATE()
and  x1.paymentDate IS NOT NULL AND x1.state = 13
GROUP BY t1.managerId)s1 on s0.managerId= s1.managerId
where IFNULL(s1.cnt2,0) < 2
-- M2
UNION ALL
select 'M2' `le`, s0.managerId,s0.cnt1,CONCAT('催回单量:',IFNULL(s1.cnt2,0)) cnt0,CONCAT(SUBDATE(CURDATE(),INTERVAL 15 DAY),' ~ ',SUBDATE(CURDATE(),INTERVAL 1 DAY)) dd
FROM (
select managerId,count(0) cnt1
from turku.urge_order_log t1
where state=2 AND time BETWEEN SUBDATE(CURDATE(),INTERVAL 15 DAY) AND CURDATE()
group by managerId HAVING cnt1> 30)s0
LEFT JOIN (
select  t1.managerId,count(0) cnt2
from turku.urge_order_log t1
left JOIN turku.urge_order x1 
on t1.orderId = x1.orderId
where t1.state=2 AND t1.time BETWEEN SUBDATE(CURDATE(),INTERVAL 15 DAY) AND CURDATE()
and  x1.paymentDate IS NOT NULL AND x1.state = 2
GROUP BY t1.managerId)s1 on s0.managerId= s1.managerId
where IFNULL(s1.cnt2,0)< 1)u1
LEFT JOIN turku.manager m on u1.managerId = m.id 
WHERE u1.managerId >0 

'''


# 催收案件分配
def collection_assign():
    task_success = False
    lv = 0
    db_turku = None
    count = []
    item = ItemEnum.collection_assign
    msg = ''
    date_msg = get_delta_date(0)
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
        # if not count[0] != 0:
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
        record_save.save_record(item, lv, task_success, date_msg, msg)
        return count


# 催收率
def collection_rate():
    task_success = False
    lv = 0
    db_turku = None
    count = []
    item = ItemEnum.collection_rate
    msg = ''
    date_msg = get_delta_date(0)
    try:
        db_turku = my_db.get_turku_db()
        if not db_turku:
            db_task.db_error()
            log.error("get db error.")
            return
        # 催收案件分配
        cursor_turku = db_turku.cursor()
        cursor_turku.execute(sql_collection_rate)
        # [催收主体名称，时间段，委案量，催回单量/催回率]
        count = cursor_turku.fetchall()
        if not count:
            raise (TaskException(item, lv, my_db.msg_data_not_exist))
        # if not count[0] != 0:
        if count:
            lv = 2
            data = [item.value.get('msg1') % (c[0], c[1], c[2], c[3]) for c in count]
            raise (TaskException(item, lv, "\n" + "".join(data)))
        task_success = True
    except TaskException as te:
        msg = te.msg
        log.error("collection_assign alarm.data:%s,lv:%d,msg:%s" % (json.dumps(count), te.level, te.msg))
    except Exception as e:
        msg = "collection_rate fail."
        log.error("collection_assign fail.data:%s,msg:%s" % (json.dumps(count), e.message))
    finally:
        if db_turku:
            db_turku.close()
        record_save.save_record(item, lv, task_success, date_msg, msg)
        return count
