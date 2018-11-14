# -*- coding: utf-8 -*-

import os
import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

conf = ConfigParser.ConfigParser()
sys = os.name
CONF_DIR = ''

if sys == 'nt':
    CONF_DIR = 'C://Users//user//Dropbox//work//yunfeng//doc//monitor//settings.ini'
    DEBUG = True
    ALLOWED_HOSTS = ['*']

elif sys == 'posix':
    CONF_DIR = '/data/config/rauma/settings.ini'
    DEBUG = False
    ALLOWED_HOSTS = ['*']

conf.read(CONF_DIR)
# 密钥
SECRET_KEY = conf.get('global', 'SECRET_KEY'),
# mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': conf.get('global', 'mysql_dbname'),
        'USER': conf.get('global', 'mysql_username'),
        'PASSWORD': conf.get('global', 'mysql_password'),
        'HOST': conf.get('global', 'mysql_host'),
        'PORT': conf.get('global', 'mysql_port'),

    }
}
# redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://" + conf.get('global', 'redis_url'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": conf.get('global', 'redis_password'),
        }
    }
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'monitor.apps.MonitorConfig',
    'django_apscheduler',
    'monitor.templatetags.my_tags',
]

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=5),  # seconds=300
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rauma.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/templates", ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'get_mon_type_name': 'monitor.templatetags.my_tags'
            }
        },
    },
]

WSGI_APPLICATION = 'rauma.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# sqlite本地调试
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "temp"),
]

# 用户插入固定的语句，如监控配置项
# 1. python manage.py dumpdata > sql.json 先导出
# 2. python manage.py loaddata item 再导入
FIXTURE_DIRS = [
    '/monitor/fixtures/',
]

import sys
import logging.config
import os
from django.utils.log import DEFAULT_LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)-8s [%(name)s:%(funcName)s:%(lineno)-3s] %(message)s",
            # 'datefmt': "%Y-%m-%d %H:%M:%S.%s"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': conf.get('global', 'log_file_path'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 100,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'monitor': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'wxpy': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

reload(sys)
sys.setdefaultencoding("utf-8")

# send e-mail
# EMAIL_HOST = 'smtp.163.com'  # smtp 地址（这里需要注意，如果你和我一样使用 163 邮箱的话，默认 smtp 功能是关闭的，需要去设置开启，并生成一个一次性密码用于连接 smtp 服务）
# EMAIL_HOST_USER = '@163.com'  # 用户
# EMAIL_HOST_PASSWORD = ''  # 密码
# EMAIL_SUBJECT_PREFIX = u'[]'  # 为邮件Subject-line前缀,默认是'[django]'
# EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false

# 生成依赖文件 pip freeze > requirements.txt
# 安装依赖文件 pip install -r requirement.txt
# 1. 执行migrate
#  python manage.py makemigrations
# python manage.py migrate
# 2.创建超级用户
# python manage.py createsuperuser
# 3.启动项目
# python manage.py runserver
