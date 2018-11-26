# -*- coding: utf-8 -*-
from base_enum import *
from enum import Enum, unique


class MonitorTypeEnum(BaseEnum):
    base = EnumType(1, u'基础')
    account = EnumType(2, u'账务系统')
    risk = EnumType(3, u'风控系统')
    third = EnumType(4, u'三方接口')


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
                      "msg1": "无注册量",
                      "msg2": "注册量%d < 昨天同比%d的30%%",
                      "mon_desc": "如果每小时注册量=0, level=1; 注册量<昨天同比30%，level=2"}
    today_loan_amount = {"id": 3,
                         "mon_type": 2,
                         "mon_title": "当日放款金额",
                         "mon_trigger": "0/30 10-23 * * *",
                         "mon_trigger_desc": "每天从10:00-00:00，每0.5小时查询一次",
                         "msg1": "放款量为0",
                         "msg2": "放款金额%.2f < 昨天同比%.2f的50%%",
                         "mon_desc": "如果放款量=0, level=1; 放款量<昨天同比50%，level=2"}
    today_repay = {"id": 4,
                   "mon_type": 2,
                   "mon_title": "当日回款",
                   "mon_trigger": "0 11-23/1 * *  *",
                   "mon_trigger_desc": "每天从12:00-00:00，每个小时查询一次",
                   "msg1": "回款量为0",
                   "msg2": "回款率%.2f%% < 昨天同比%.2f%%的30%%",
                   "msg3": "回款率%.2f%%",
                   "mon_desc": "如果回款量=0, level=1; 回款率<昨天同比30%，level=2;23:00时的回款率<60%, level=2;"}
    repayment_sms = {"id": 5,
                     "mon_type": 2,
                     "mon_title": "还款短信和语音提醒",
                     "mon_trigger": "30 9,15 * *  *",
                     "mon_trigger_desc": "每天9:30检查一次",
                     "msg1": "【短信】应提醒%d，实际提醒%d,成功率%.2f%%",
                     "msg2": "【语音】应提醒%d，成功%d,成功率%.2f%%",
                     "mon_desc": "短信（T、T-1）成功率0.8；语音首次成功率0.2，level=2;"}
    collection_assign = {"id": 6,
                         "mon_type": 2,
                         "mon_title": "催收案件分配",
                         "mon_trigger": "30 9 * *  *",
                         "mon_trigger_desc": "每天9:30检查一次",
                         "msg1": "没有催收案件分配",
                         "mon_desc": "催收案件每个managerId都有分配，level=2;"}
    account_balance = {"id": 7,
                       "mon_type": 2,
                       "mon_title": "账户余额",
                       "mon_trigger": "0 0/1 * * *",
                       "mon_trigger_desc": "每1个小时检查一次",
                       "msg1": "当前易宝账户余额%0.2f < 昨天同期下2个小时放款量%.2f 的1.5倍",
                       "mon_desc": "如果当前易宝账户余额<昨天同期下2个小时放款量的1.5倍，则level 1;"}
    risk_pass_rate = {"id": 8,
                      "mon_type": 3,
                      "mon_title": "通过率检查",
                      "mon_trigger": "0/30 9-23 * * *",
                      "mon_trigger_desc": "每天从9:00开始每0.5小时查询一次",
                      "msg1": "\n【注册放款率】%.2f%%\n【审核通过率】%.2f%%",
                      "mon_desc": "当日的注册数>50的情况下，注册放款率或者审核通过率=0，level=1；注册放款率<5%或者审核通过率<10%, level=2;"}
    fail_reason = {"id": 9,
                   "mon_type": 3,
                   "mon_title": "failReason异常检查",
                   "mon_trigger": "0 9-23/1 * * *",
                   "mon_trigger_desc": "每天从9:00开始每1小时查询一次",
                   "msg1": "【%s】%.2f%%\n",
                   "mon_desc": "failreaon占比>30%，level=2;"}
    pass_loan_rate = {"id": 10,
                      "mon_type": 3,
                      "mon_title": "通过借款率监控",
                      "mon_trigger": "0 0,9-23/1 * * *",
                      "mon_trigger_desc": "每天从9:00开始每1小时查询一次",
                      "msg1": "【%s】%.2f%%\n",
                      "mon_desc": "当日的某个渠道的通过数>=10的情况下，借款率>=90%，level=2"}
    overdue_rate_m1 = {"id": 11,
                       "mon_type": 3,
                       "mon_title": "渠道首逾监控",
                       "mon_trigger": "1 0 * * *",
                       "mon_trigger_desc": "每天00:01查询一次",
                       "msg1": "【%s】%.2f%%\n",
                       "mon_desc": "昨日应还的某个渠道的借款数>=8，并且自然还款率<=50%，level=2;"}
