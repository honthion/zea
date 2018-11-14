import requests
import json
from monitor.my_util import my_conf
import record_save
from monitor.pojo.my_enum import *

import logging
import monitor.my_util.my_db as my_db

log = logging.getLogger(__name__)


def today_register():
    content = ''
    status_code = -1
    task_success = True
    db = None
    try:
        db = my_db.get_db()
        cursor =  db.cursor()
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
        raw = cursor



    except Exception:
        log.error("account_login response.status_code :%d,content:%s" % (status_code, content))
        task_success = False
    finally:
        if db:
            db.close()
    record_save.save_record(ItemEnum.base_task, task_success, "status_code:%s;content:%s" % (status_code, content))
