'''
Author: 邹洋
Date: 2021-08-14 09:56:23
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-06 21:50:10
Description: 工具类
'''

import time

import requests
from ChileCat.settings import DEBUG
token = '10218bcad82e4ddfb842b47d358334fa'
url = 'http://pushplus.hxtrip.com/send'
def push_wx(title,content,template='html'):
    if DEBUG == False:
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
