'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-05 19:29:22
Description: 控制用户是否能访问URL地址
'''
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser, Permission


class ApiPublicPermission(BasePermission):
    message = '没有权限'

    def has_permission(self, request, view):
        
        return True
        url = request.META['PATH_INFO']
        method = request.META['REQUEST_METHOD']

        if request.user.is_superuser:
            return True

        url_permission = url + ':' + method
        auth_error = '用户认证失败'
        
        # 白名单功能
        api_per = Permission.objects.filter(codename=url_permission, api_permission__is_verify__in=[1,2])
        if api_per.exists():
            if api_per[0].api_permission.is_verify==1:
                if request.user == AnonymousUser:
                    self.message = auth_error
                    return False
            return True

        # 是否登录
        if request.user == AnonymousUser:
            self.message = auth_error
            return False

        # 权限验证
        if request.user.has_perm('Permission.' + url_permission):
            return True

        return False
