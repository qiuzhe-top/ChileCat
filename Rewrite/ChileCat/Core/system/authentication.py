'''
Author: 邹洋
Date: 2022-02-06 21:58:29
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 14:44:19
Description: 
'''
from rest_framework.authentication import BaseAuthentication
from AppUser import models
from django.contrib.auth.models import AnonymousUser


class AuthPermission(BaseAuthentication):

    def authenticate(self, request):
        # 查找是否有匹配Token
        token = models.Token.objects.filter(
            token=request.META.get("HTTP_TOKEN")).first()
        if not token:
            return AnonymousUser, None
        return token.user, None