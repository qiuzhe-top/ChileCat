'''
Author: 邹洋
Date: 2022-02-12 22:12:13
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-13 19:51:43
Description: 开发环境
'''
from .base import *
DEBUG = True
password = 'Zhou24272592.'
host = '124.223.43.151'
# WebSocket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        "TIMEOUT": None,
        'CONFIG': {
            "hosts": ["redis://:"+password+"@"+host+":6379/2"],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    },
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://"+host+":6379/1",
        "TIMEOUT": None,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": password,
            "CONNECTION_POOL_KWARGS": {"decode_responses": True,"max_connections": 200},
        }
    }
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ChileCat',
        'USER': 'root',
        'PASSWORD': password,
        'HOST': host,
        'PORT': '3306',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
            'isolation_level': None
        },
    }
}