'''权限'''
from rest_framework.permissions import BasePermission
# from rest_framework import exceptions
# from Apps.User import models as UserModel
# from django.contrib.auth.models import AnonymousUser
from Apps.Permission import models
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
        if request.user.userinfo.user_role.filter(name="root").exists():
            return True

        url = request.META['PATH_INFO']
        method = request.META['REQUEST_METHOD']
        control_obj = models.ApiPermission.objects.filter(url=url,method=method)
        if not control_obj.exists():
            print("此接口没有开放权限,请联系管理员")
            return False
        try:
            if request.user.userinfo.user_role.filter(
                role_permit=control_obj.first().per_id
                ).exists():
                return True
            ApiPermission.message="没有权限"
            return False
        except AttributeError:
            ApiPermission.message = "用户未登录"
            return False
        print("接口权限：全局API接口权限")
        return True
