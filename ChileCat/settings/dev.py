'''
Author: 邹洋
Date: 2022-02-12 22:12:23
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-03-17 20:24:34
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
        'NAME': 'ChileCatTest',
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

# 日志配置
log_path = 'D:\\code\\Cat\\ChileCatLog\\'# os.path.join(os.path.dirname(current_path), 'logs') # 日志存放目录
if not os.path.exists(log_path): os.mkdir(log_path) # 若目录不存在则创建

LOGGING = {
    'version':1,# 版本
    'disable_existing_loggers':False, # 是否禁用已存在的日志器
    # 日志格式
    'formatters': {
        'standard':{
            'format':'[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                     '[%(levelname)s]- %(message)s'
        },
        'simple':{
            'format':'%(levelname)s %(module)s %(lineno)d %(message)s'
        },
        'verbose':{
            'format':'%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true':{
            '()':'django.utils.log.RequireDebugTrue'
        }
    },
    # 处理器
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'all-{}.log'.format(time.strftime('%Y-%m'))),
            'maxBytes': 1024 * 1024 * 30,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
 
    },
    # 配置日志处理器
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',  # 日志器接收的最低日志级别
            'propagate': True,
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
    }
}
# from Core.utils import logger
# logger.exception_handler(111)
# pip install uvicorn
# uvicorn ChileCat.asgi:application --host '0.0.0.0' --port 8000 --reload