import configparser
from rauma import settings

cf = configparser.ConfigParser()
conf_path = settings.CONF_DIR
cf.read(conf_path)
# truku data base config
turku_mysql_host = cf.get("turku_data_base", "mysql_host")

turku_mysql_username = cf.get("turku_data_base", "mysql_username")

turku_mysql_password = cf.get("turku_data_base", "mysql_password")

turku_mysql_port = cf.get("turku_data_base", "mysql_port")

turku_mysql_dbname = cf.get("turku_data_base", "mysql_dbname")

turku_login_url = cf.get("turku_host", "host") + cf.get("turku_host", "login_api")

notify_email_subject = cf.get("monitor_notify", "email_subject")

notify_email_manager = cf.get("monitor_notify", "email_manager")
