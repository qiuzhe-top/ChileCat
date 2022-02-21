'''
Author: 邹洋
Date: 2022-02-06 21:58:29
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-17 14:05:10
Description: 
'''
from rest_framework.authentication import BaseAuthentication
from AppUser import models
from django.contrib.auth.models import AnonymousUser


class AuthPermission(BaseAuthentication):

    def authenticate(self, request):
        token_str = request.META.get("HTTP_TOKEN",-1)
        token_get = request.GET.get('token',-1)
        token = models.Token.objects.filter(token__in=[token_str,token_get]).first()
        if not token:
            return AnonymousUser, None
        return token.user, None