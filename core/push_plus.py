'''
Author: 邹洋
Date: 2021-12-14 10:09:15
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-12-14 12:13:47
Description: 公众号消息推送
'''

import requests

token = '10218bcad82e4ddfb842b47d358334fa'
url = 'http://pushplus.hxtrip.com/send'
def push_wx(title,content,template='html'):
    data = {
        'token':token,
        'title':title,
        'content':content,
        'template':template
    }
    requests.post(url,data)