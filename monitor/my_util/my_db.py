import MySQLdb
from django.db import connections


def get_db():
    MySQLdb.connect(host="localhost",  # your host, usually localhost
                    user="john",  # your username
                    passwd="megajonhy",  # your password
                    db="jonhydb")  # name of the data base


# https://blog.csdn.net/little_stupid_child/article/details/81774194  OperationalError: (2006, 'MySQL server has gone away')
def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()
