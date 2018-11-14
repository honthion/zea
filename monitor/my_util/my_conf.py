import configparser
from rauma import settings

cf = configparser.ConfigParser()
conf_path = settings.CONF_DIR
print conf_path
cf.read(conf_path, encoding='UTF-8')
# truku data base config
turku_mysql_host = cf.get("turku_data_base", "mysql_host").encode('unicode-escape').decode('string_escape')

turku_mysql_username = cf.get("turku_data_base", "mysql_username").encode('unicode-escape').decode('string_escape')

turku_mysql_password = cf.get("turku_data_base", "mysql_password").encode('unicode-escape').decode('string_escape')

turku_mysql_port =int( cf.get("turku_data_base", "mysql_port").encode('unicode-escape').decode('string_escape'))

turku_mysql_dbname = cf.get("turku_data_base", "mysql_dbname").encode('unicode-escape').decode('string_escape')

turku_login_url = cf.get("turku_host", "host") + cf.get("turku_host", "login_api")

wx_corpid = cf.get("weixin", "corpid").encode('unicode-escape').decode('string_escape')

wx_mjb_agentid_lv0 = "1000007"

wx_mjb_secret_lv0 = "VCwQjldxu2th0UvWTaU0RvOPIP-4WbCdp1BACBwsB10"

wx_mjb_agentid_lv1 = cf.get("weixin", "mjb_agentid_lv1").encode('unicode-escape').decode('string_escape')

wx_mjb_secret_lv1 = cf.get("weixin", "mjb_secret_lv1").encode('unicode-escape').decode('string_escape')

wx_mjb_agentid_lv2 = cf.get("weixin", "mjb_agentid_lv2").encode('unicode-escape').decode('string_escape')

wx_mjb_secret_lv2 = cf.get("weixin", "mjb_secret_lv2").encode('unicode-escape').decode('string_escape')

wx_get_token_url = cf.get("weixin", "get_token_url").encode('unicode-escape').decode('string_escape')

wx_apply_info_url = cf.get("weixin", "apply_info_url").encode('unicode-escape').decode('string_escape')

wx_send_msg_url = cf.get("weixin", "send_msg_url").encode('unicode-escape').decode('string_escape')

wx_get_label_list = cf.get("weixin", "get_label_list").encode('unicode-escape').decode('string_escape')

base_url = cf.get("global", "base_url").encode('unicode-escape').decode('string_escape')
