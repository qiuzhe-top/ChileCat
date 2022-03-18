'''
Author: 邹洋
Date: 2022-02-12 22:12:23
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-03-18 09:01:00
Description: 线上环境
'''
from .base import *
DEBUG = False
ASGI_APPLICATION = 'ChileCat.asgi.application'


password = 'Zhou24272592.' 
host = '127.0.0.1'
redis_password = password
redis_host = "redis://:"+redis_password+"@"+host+":6379"
sql_host = host
sql_password = password
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [redis_host + "/2"]
CACHES['default']['LOCATION'] =  redis_host + "/1"
CACHES['default']['OPTIONS']['PASSWORD'] =  redis_password
DATABASES['default']['PASSWORD'] = sql_password
DATABASES['default']['HOST'] = sql_host
# pip install uvicorn
# uvicorn ChileCat.asgi:application --host '0.0.0.0' --port 8000 --reload