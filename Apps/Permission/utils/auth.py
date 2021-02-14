'''用户认证'''
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
from Apps.User import models as UserModel
from django.contrib.auth.models import AnonymousUser
# from Apps.Permission.models import ApiPermission
# 
class AuthPermission(BaseAuthentication):
    '''
        全局身份标识
    '''
    def authenticate(self,request):
        token = request.META.get("HTTP_TOKEN")
        token_obj = UserModel.Token.objects.filter(token = token).first()
        if not token_obj:
            return (AnonymousUser,None)
        return (token_obj.user.django_user,None)

class AuthPer(BaseAuthentication):
    '''
        局部身份认证
    '''
    def authenticate(self,request):
        token = request.META.get("HTTP_TOKEN")
        token_obj = UserModel.Token.objects.filter(token = token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return (token_obj.user.django_user,None)
