# -*- coding: utf-8 -*-
from base_enum import *
from enum import Enum, unique


class MonitorTypeEnum(BaseEnum):
    base = EnumType(1, u'基础')
    account = EnumType(2, u'账务系统')
    risk = EnumType(3, u'风控系统')
    third = EnumType(4, u'三方接口')

    STATUS_CHOICE = (
        (1, u'正常'),
        (2, u'告警中'),
        (3, u'恢复'),
    )


class MonitorStatusEnum(BaseEnum):
    normal = EnumType(1, u'正常')
    alarm = EnumType(2, u'告警中')
    recovery = EnumType(3, u'恢复')


@unique
class ItemEnum(Enum):
    base_task = {"id": 1,
                 "mon_type": 1,
                 "mon_title": "账户登陆",
                 "mon_trigger": "0/5 * * * *",
                 "mon_trigger_desc": "轮询每隔5分钟",
                 "msg1": "无法登陆",
                 "mon_desc": "模拟用户登陆，如果无法登陆，则告警level=1"}
    today_register = {"id": 2,
                      "mon_type": 2,
                      "mon_title": "当日注册用户",
                      "mon_trigger": "0/30 10-23 * * *",
                      "mon_trigger_desc": "每天从10:00-00:00，每0.5小时查询一次",
                      "msg1": "前一小时无注册量",
                      "msg2": "注册量 < 昨天同比30%",
                      "mon_desc": "如果每小时注册量=0, level=1; 注册量<昨天同比30%，level=2"}
    today_loan_amount = {"id": 3,
                         "mon_type": 2,
                         "mon_title": "当日放款金额",
                         "mon_trigger": "0/30 9-23 * * *",
                         "mon_trigger_desc": "每天从10:00-00:00，每0.5小时查询一次",
                         "msg1": "前一小时放款量=0",
                         "msg2": "放款量<昨天同比50%",
                         "mon_desc": "如果放款量=0, level=1; 放款量<昨天同比50%，level=2"}
    today_repay = {"id": 4,
                          "mon_type": 2,
                          "mon_title": "当日回款",
                          "mon_trigger": "56 12-23/1 * *  *",
                          "mon_trigger_desc": "每天从12:00-00:00，每个小时查询一次",
                          "msg1": "前一小时回款量=0",
                          "msg2": "回款率<昨天同比30%",
                          "msg3": "23:00时的回款率 < 60%",
                          "mon_desc": "如果回款量=0, level=1; 回款率<昨天同比30%，level=2；23:00时的回款率<60%, level=2;"}
