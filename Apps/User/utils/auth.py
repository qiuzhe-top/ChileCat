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
class TokenAuth(BaseAuthentication):
    '''
    Token
    '''
    def authenticate(self,request):
        #判断是否在headers携带token
        token = request.META.get("HTTP_TOKEN")
        # token = request._request.GET.get('token')
        token_obj = models.User_Token.objects.filter(token = token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        #在rest 内部会把他们给request
        return (token_obj.user,token_obj)
    def authenticate_header(self,request):
        pass



def get_token(request):
    '''
    获取token
    '''
    try:
        token = request.META.get("HTTP_TOKEN")
        print(token)
    except KeyError as identifier:
        print(identifier,'no token')
    return token

def get_user(request):
    '''
    获取用户
    '''
    return request.user
    # try:
    #     token = get_token(request)
    #     print("获得的token: ",token)
    #     obj = models.Token.objects.get(token=token)
    #     # print(obj)
    #     return obj.user
    # except ObjectDoesNotExist as token_not_exist:
    #     print(token_not_exist,"not get user ")
    #     return -1
    # return 1


def md5(user):
    '''
    获取md5
    '''
    ctime = str(time.time())
    get_md5 = hashlib.md5(bytes(str(id(user)), encoding='utf-8'))
    get_md5.update(bytes(ctime, encoding='utf-8'))
    return get_md5.hexdigest()

def update_token(user_account_obj):
    '''
    更新token
    '''
    token = md5(user_account_obj)
    token_obj,b = models.Token.objects.get_or_create(user_id=user_account_obj.id)
    token_obj.token = token
    token_obj.save()
    return token