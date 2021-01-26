from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from Apps.User import models as UserModel
# 全局API接口权限
class ApiPermission(BasePermission):
  '''
  场景：
    用户A： 角色：查寝管理人员
    用户B： 角色：辅导员
    接口1： 刷新验证码接口
    接口2： 获取今日新闻信息
  实现：  
    功能1：A有权访问接口1，B拒绝访问
    功能2：A B 都能访问接口2

  逻辑：
    url : 当前访问地址
    method : 当前访问的方法
    url_per : 当前url对应的权限   （用url去ApiPer表里面拿到Permission表里的权限对象）
    user_per_list : 当前用户拥有的所有角色下的权限列表 (Permission表里的权限对象)
    if url_per in user_per_list:
      return True #实现功能1
    else:
      return False


    当url不在ApiPer表里面表示这个接口为公共接口 直接放行 实现功能2
  '''
  message = '访问接口失败'

  def has_permission(self, request, view):
      """
      只有拥有当前api权限的用户通过
      """

      print("接口权限：全局API接口权限")
      return True

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
    if url in ApiPer表:
      直接调用 TokenAuthFunction(request)
    else:
      raise exceptions.AuthenticationFailed('用户认证失败')
  '''
  def authenticate(self,request):
      print("登录验证：全局登录验证")
      pass

  def authenticate_header(self,request):
      pass

# 局部登录验证
class TokenAuth(BaseAuthentication):
  '''
  基于token的登录验证
  在 View 里面使用的时候会覆盖全局登录验证
  用来对单个View进行控制

  功能已完成
  '''
  def authenticate(self,request):
      print("登录验证：局部登录验证")
      TokenAuthFunction(request)

  def authenticate_header(self,request):
      pass

# 身份登录验证逻辑
def TokenAuthFunction(request):
    token = request.META.get("HTTP_TOKEN")
    token_obj = UserModel.Token.objects.filter(token = token).first()
    if not token_obj:
        raise exceptions.AuthenticationFailed('用户认证失败')
    #在rest 内部会把他们给request
    return (token_obj.user,token_obj)