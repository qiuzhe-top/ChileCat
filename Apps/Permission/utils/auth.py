'''用户认证'''
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from Apps.User import models as UserModel
from Apps.Permission.models import ApiPermission
from django.contrib.auth.models import AnonymousUser
# from Apps.Permission.models import ApiPermission
# 全局登录验证
class AuthPermission(BaseAuthentication):
    '''
        所有接口和操作默认需要身份验证
    '''
    def authenticate(self,request):
        url = request.META['PATH_INFO']
        method = request.META['REQUEST_METHOD']
        #TODO(liuhai) 白名单返回None用户为后台的permission做权限判断(注意这是不稳妥的)

        # print("登录验证：全局登录验证")
        return token_auth_function(request)

# 身份登录验证逻辑
def token_auth_function(request):
    '''身份登录验证逻辑'''
    token = request.META.get("HTTP_TOKEN")
    token_obj = UserModel.Token.objects.filter(token = token).first()
    url = request.META['PATH_INFO']
    method = request.META['REQUEST_METHOD']
    if url_write_list(url,method):
        return (AnonymousUser,None)
    if not token_obj:
        raise exceptions.AuthenticationFailed('用户认证失败')
    return (token_obj.user.django_user,None)

def url_write_list(url,method):
    '''判断访问的url是否在白名单(只判断url)'''
    url = ApiPermission.objects.filter(url=url,method=method)
    if url.exists():
        url_per = url.first().per_id.role.filter(name="白名单")
        if url_per.exists():
            return True
        return False
    return False
