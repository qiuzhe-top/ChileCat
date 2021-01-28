'''权限'''
from rest_framework.permissions import BasePermission
# from rest_framework import exceptions
# from Apps.User import models as UserModel
# from django.contrib.auth.models import AnonymousUser
from Apps.Permission import models
# 全局API接口权限
class ApiPermission(BasePermission):
    '''
        api权限,用来验证用户是否有权限访问对应的api
    '''
    message = '访问接口失败'
    def has_permission(self, request, view):
        """
        只有拥有当前api权限的用户通过
        """
        if request.user is None:
            return True
        url = request.META['PATH_INFO']
        method = request.META['REQUEST_METHOD']
        control_obj = models.ApiPermission.objects.filter(url=url,method=method)
        try:
            if request.user.userinfo.user_role.filter(name="root").exists():
                return True
            if not control_obj.exists():
                ApiPermission.message = "此接口没有开放权限,请联系管理员"
                print("此接口没有开放权限,请联系管理员")
                return False
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
