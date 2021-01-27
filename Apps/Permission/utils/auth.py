'''用户认证'''
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from Apps.User import models as UserModel
from Apps.Permission.models import ApiPermission
# 全局登录验证
class AuthPermission(BaseAuthentication):
    '''
    需求:
        全局登录验证只对ApiPer表内存在的接口进行登录验证
        在进行Api权限验证时，当前用户肯定为登录用户
        所以需要在访问 需要权限Api接口前 进行登录验证 (且验证为全局性验证)
    逻辑：
        url : 当前访问地址
        method : 当前访问的方法
        if url in API权限表:
        直接调用 TokenAuthFunction(request)
        else:
        raise exceptions.AuthenticationFailed('用户认证失败')
    '''
    def authenticate(self,request):
        print("登录验证：全局登录验证")
        return token_auth_function(request)


# 身份登录验证逻辑
def token_auth_function(request):
    '''身份登录验证逻辑'''
    token = request.META.get("HTTP_TOKEN")
    token_obj = UserModel.Token.objects.filter(token = token).first()
    if not token_obj:
        raise exceptions.AuthenticationFailed('用户认证失败')
    return (token_obj.user,None)
