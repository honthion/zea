import requests
import json
from monitor.my_util import my_conf
import record_save
from monitor.pojo.my_enum import *
from monitor.my_util.time_util import *
import logging

log = logging.getLogger(__name__)


def account_login():
    content = ''
    status_code = -1
    task_success = True
    item = ItemEnum.base_task
    lv = 0
    msg = ''
    date_msg = get_date_time_now()
    try:
        request_body = {'cellphone': '13261575028', 'password': 'fae262e4c1e545642eed8d3a3e8fd89f', 'type': 0,
                        'secretKey': '059b668ae94237c2fbe64df4198e1a00', "os_version": "8.1.0", "os_name": "BLA-AL00",
                        "platform": "Android"}
        url = my_conf.turku_login_url
        log.info("account_login request. url:%s,request_body:%s" % (url, request_body))
        r = requests.post(url, data=request_body)
        status_code = r.status_code
        content = r.content
        log.info("account_login response.status_code :%d,content:%s" % (status_code, content))
        assert status_code == 200
        assert content != ''
        response_body = json.loads(content)
        assert response_body.get('errcode') == 0
        # assert 1 == 0
    except Exception:
        log.error("account_login response.status_code :%d,content:%s" % (status_code, content))
        lv = 1
        msg = item.value.get('msg1')
        task_success = False
    record_save.save_record(ItemEnum.base_task, lv, task_success, date_msg, msg)
