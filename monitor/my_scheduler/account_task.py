# -*- coding: utf-8 -*-
import requests
import json
from monitor.my_util import my_conf
import record_save
from monitor.pojo.my_enum import *
import monitor.my_scheduler.db_task as db_task
import logging
import monitor.my_util.my_db as my_db
from monitor.pojo.my_exception import *

log = logging.getLogger(__name__)


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
        count = [1, 2, 10]
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
