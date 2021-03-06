'''
Author: 邹洋
Date: 2021-08-14 09:56:23
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-03-17 20:17:48
Description: 工具类
'''

import logging
import time

import requests
from django.conf import settings

logger = logging.getLogger('log')

token = '10218bcad82e4ddfb842b47d358334fa'
url = 'http://pushplus.hxtrip.com/send'
def push_wx(title,content,template='html'):
    if settings.DEBUG == False:
        data = {
            'token':token,
            'title':title,
            'content':content,
            'template':template
        }
        requests.post(url,data)
        
def time_start():
    return time.time()

def time_end(t,str='耗时'):
    print(f'{str}:{time.time() - t:.8f}s')


def is_number(s):
    '''判断字符串是否为数字'''
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def info(msg):
    logger.info(msg)

def error(msg):
    logger.error(msg)

def console(msg):
    logger.log
    logger.console(msg)