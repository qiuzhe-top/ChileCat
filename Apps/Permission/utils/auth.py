'''用户认证'''
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from Apps.User import models as UserModel
# from Apps.Permission.models import ApiPermission
class AuthPermission(BaseAuthentication):
    '''
        全局身份标识
    '''
    def authenticate(self,request):
        if str(request.META.get("HTTP_TOKEN")) == "000":
            return (None,None)
        token = UserModel.Token.objects.filter(
            token = request.META.get("HTTP_TOKEN")).first()
        if not token:
            return(AnonymousUser,None)
        return (token.user,None)

class AuthPer(BaseAuthentication):
    '''
        身份认证
    '''
    def authenticate(self,request):
        token =  UserModel.Token.objects.filter(
            token = request.META.get("HTTP_TOKEN")).first()
        if not token:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return (token.user,None)
