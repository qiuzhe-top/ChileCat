'''
用户登录接口
'''
# import json
# import os
# import time
import hashlib
import time
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.core.exceptions import ObjectDoesNotExist
from Apps.User import models


def get_token(request):
    """
    获取token
    """
    try:
        token = request.META.get("HTTP_TOKEN")
        print(token)
    except KeyError as identifier:
        print(identifier, 'no token')
    return token


def get_user(request):
    """
    获取用户
    """
    return request.user


def get_groups(request):
    """
    获取用户身份组
    """
    per = request.user.groups.all().values('name')
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
    return token
