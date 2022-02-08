'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-11 14:26:03
Description: 
'''
"""
用户登录接口
"""

import hashlib
import time
from Apps.User import models


def get_token(request):
    """
    获取token
    """
    try:
        token = request.META.get("HTTP_TOKEN")
        print(token)
        return token
    except KeyError as identifier:
        print(identifier, 'no token')

def get_token_by_user(request):
    token = request.params.token
    user = models.Token.objects.get(token=token).user
    request.user = user
    return user

def get_user(request):
    """
    获取用户
    """
    return request.user


def get_groups(user):
    """
    获取用户身份组
    """
    per = user.groups.all().values('name')
    groups = []
    for item in per:
        groups.append(item['name'])
    return groups


def md5(user):
    """
    获取md5
    """
    ctime = str(time.time())
    get_md5 = hashlib.md5(bytes(str(id(user)), encoding='utf-8'))
    get_md5.update(bytes(ctime, encoding='utf-8'))
    return get_md5.hexdigest()


def update_token(user_account_obj):
    """
    更新token
    """
    token = md5(user_account_obj)
    token_obj, b = models.Token.objects.get_or_create(user_id=user_account_obj.id)
    token_obj.token = token
    token_obj.save()
    return token_obj
