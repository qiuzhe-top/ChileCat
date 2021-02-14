'''权限'''
from Apps.Permission import models
from Apps.Permission.models import ApiPermission
from django.contrib.auth.models import AnonymousUser, Permission, User
from django.http import JsonResponse
from rest_framework.permissions import BasePermission

# 全局API接口权限
class ApiPublicPermission(BasePermission):
    '''
        api权限,用来验证用户是否有权限访问对应的api
    '''
    message = '没有权限'
    def has_permission(self, request, view):
        """
        只有拥有当前api权限的用户通过
        """
        url = request.META['PATH_INFO']
        method = request.META['REQUEST_METHOD']

        if request.user.is_superuser:
            return True

        url_permission = url + ':' + method

        # 白名单功能
        if Permission.objects.filter(codename = url_permission,apipermission__is_verify = True).exists():
            return True

        # 是否登录
        if request.user == AnonymousUser:
            self.message = '用户认证失败'
            return False 

        # 权限验证
        if request.user.has_perm('Permission.'+url_permission):
            return True

        return False




