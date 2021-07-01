"""权限"""
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser, Permission


# 全局API接口权限
class ApiPublicPermission(BasePermission):
    """
        api权限,用来验证用户是否有权限访问对应的api
    """
    message = '没有权限'

    def has_permission(self, request, view):
        """
        只有拥有当前api权限的用户通过
        """
        # return True
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
