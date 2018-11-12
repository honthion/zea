# -*- coding: utf-8 -*-

"""
Django settings for rauma project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# CONF_DIR = 'C:\Users\user\Dropbox\work\yunfeng\doc\monitor\setting.ini'
# CONF_DIR = '/data/config/rauma/setting.ini'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '*l-azd7kg_a)c3&ukm%eucz7rf#niyj+l^h@orf4+=uqv^2uu('
SECRET_KEY = 'cm*oz%(rg6s#b%s_$gd4#zbc2ud(2m38czmpf*dcubw+f8t7#m'


sys = os.name
if sys == 'nt':
    CONF_DIR = 'C:\Users\user\Dropbox\work\yunfeng\doc\monitor\setting.ini'
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'polls',
            'USER': 'mysql',
            'PASSWORD': '123456',
            'HOST': '172.16.50.112',
            'PORT': '3306',

        }
    }
elif sys == 'posix':
    CONF_DIR = '/data/config/rauma/setting.ini'
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'rauma',
            'USER': 'miaojiebeijiankong_rw',
            'PASSWORD': 'Njk5NjNlYjk5M2Nk',
            'HOST': '172.16.50.131',
            'PORT': '3306',

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
# STATIC_ROOT = 'static'

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
            'format': "[%(asctime)s] %(levelname)-8s [%(name)-12s:%(lineno)-4s] %(message)s",
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
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/log",
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
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
            # Avoid double logging because of root logger
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
EMAIL_HOST = 'smtp.163.com'  # smtp 地址（这里需要注意，如果你和我一样使用 163 邮箱的话，默认 smtp 功能是关闭的，需要去设置开启，并生成一个一次性密码用于连接 smtp 服务）
EMAIL_HOST_USER = '18623001528@163.com'  # 用户
EMAIL_HOST_PASSWORD = '881020Aa'  # 密码
EMAIL_SUBJECT_PREFIX = u'[321]'  # 为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false

# 生成依赖文件 pip freeze > requirements.txt
# 安装依赖文件 pip install -r requirement.txt
# 1. 执行migrate
#  python manage.py makemigrations
# python manage.py migrate
# 2.创建超级用户
# python manage.py createsuperuser
# 3.启动项目
# python manage.py runserver
