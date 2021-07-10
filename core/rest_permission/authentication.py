'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors: OBKoro1
LastEditTime: 2021-07-04 14:12:43
Description: 验证是否登录
'''
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from Apps.User import models as UserModel


# from Apps.Permission.models import ApiPermission
class AuthPermission(BaseAuthentication):

    def authenticate(self, request):
        if str(request.META.get("HTTP_TOKEN")) == "000":
            return None, None
        # 查找是否有匹配Token
        token = UserModel.Token.objects.filter(
            token=request.META.get("HTTP_TOKEN")).first()
        if not token:
            return AnonymousUser, None
        return token.user, None