'''
Author: 邹洋
Date: 2022-02-12 22:12:23
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-28 15:23:19
Description: 线上环境
'''
from .base import *
DEBUG = True
ASGI_APPLICATION = 'ChileCat.asgidev.application'


password = 'Zhou24272592.' 
host = '127.0.0.1'
 
redis_password = ''
redis_host = "redis://:"+redis_password+"@"+'124.223.43.151'+":8379"

sql_host = host
sql_password = password

# WebSocket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        "TIMEOUT": None,
        'CONFIG': {
            "hosts": [redis_host + "/2"],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    },
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": redis_host + "/1",
        "TIMEOUT": None,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": redis_password,
            "CONNECTION_POOL_KWARGS": {"decode_responses": True,"max_connections": 200},
        }
    }
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ChileCat',
        'USER': 'root',
        'PASSWORD': sql_password,
        'HOST': sql_host,
        'PORT': '3306',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
            'isolation_level': None
        },
    }
}
# pip install uvicorn
# uvicorn ChileCat.asgi:application --host '0.0.0.0' --port 8000 --reload