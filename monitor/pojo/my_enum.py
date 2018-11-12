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
                 "mon_trigger": "0/1 * * * *",
                 "mon_trigger_desc": "轮询每隔5分钟",
                 "mon_desc": "模拟用户登陆，如果无法登陆，则告警level=1"}

    # today_register_account = Item(id=2,
    #                               mon_type=2,
    #                               mon_title="当日注册用户",
    #                               mon_trigger="*/30 10-23 * * *",
    #                               mon_trigger_desc="每天从10:00-00:00，每0.5小时查询一次",
    #                               mon_desc="如果每小时注册量=0, level=1; 注册量<昨天同比30%，level=2")
    # today_loan_amount = Item(id=3,
    #                          mon_type=2,
    #                          mon_title="当日放款金额",
    #                          mon_trigger="0 12-23/1 * *  *",
    #                          mon_trigger_desc="每天从12:00-00:00，每个小时查询一次",
    #                          mon_desc="如果回款量=0, level=1; 回款率<昨天同比30%，level=2；23:00时的回款率<60%, level=2;")
    # repay_sms = Item(id=4,
    #                  mon_type=2,
    #                  mon_title="还款短信和语音提醒",
    #                  mon_trigger="30 9 * * *",
    #                  mon_trigger_desc="每天9:30检查",
    #                  mon_desc="如果没有发送提醒短信或者没有发送语音提醒，level=2")
    # collection_assign = Item(id=5,
    #                          mon_type=2,
    #                          mon_title="催收案件分配",
    #                          mon_trigger="30 9 * * *",
    #                          mon_trigger_desc="每天9:30检查",
    #                          mon_desc="如果没有催收案件分配，level=2")
    # account_balance = Item(id=6,
    #                        mon_type=2,
    #                        mon_title="账户余额",
    #                        mon_trigger="0 */1 * * *",
    #                        mon_trigger_desc="每1个小时检查一次",
    #                        mon_desc="如果当前易宝账户余额<昨天同期下2个小时放款量的1.5倍，则level 1")
    # pass_rate = Item(id=72,
    #                  mon_type=3,
    #                  mon_title="通过率检查",
    #                  mon_trigger="*/30 9-23 * *",
    #                  mon_trigger_desc="每天从9:00开始每0.5小时查询一次",
    #                  mon_desc="当日的注册数>50的情况下，注册放款率或者审核通过率=0，level=1；注册放款率<5%或者审核通过率<10%, level=2")
    # fail_reason = Item(id=8,
    #                    mon_type=3,
    #                    mon_title="failReason异常检查",
    #                    mon_trigger="0 9-23 * *",
    #                    mon_trigger_desc="每天从9:00开始每1小时查询一次",
    #                    mon_desc="每个failreason的数量>10的情况下，该failreaon占比比前3天同期的变化率>50%，level=2")
    # interface_call = Item(id=9,
    #                       mon_type=4,
    #                       mon_title="接口调用检查",
    #                       mon_trigger="*/30 * * * *",
    #                       mon_trigger_desc="每0.5小时检查一次",
    #                       mon_desc="每个第三方接口调用最近的0.5个小时的调用里有错误，且最后一次调用错误，则level=1；如果有错误，但最后一次调用ok，则level=2")
