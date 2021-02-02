'''权限'''
from rest_framework.permissions import BasePermission
# from rest_framework import exceptions
# from Apps.User import models as UserModel
from django.contrib.auth.models import AnonymousUser
from Apps.Permission import models
from Apps.Permission.models import ApiPermission

# from Apps.Permission.utils.auth import url_write_list
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
        
        if url_write_list(url,method):
            return True
            
        if request.user == AnonymousUser:
            self.message = '未登录'
            return False 

        control_obj = models.ApiPermission.objects.filter(url=url,method=method)
        if request.user.user.userinfo.user_role.filter(name="root").exists():
            return True
        if not control_obj.exists():
            self.message = "此接口没有开放权限,请联系管理员"
            print("此接口没有开放权限,请联系管理员")
            return False
        if request.user.user.userinfo.user_role.filter(
            role_permit=control_obj.first().per_id
            ).exists():
            return True
        return False

def url_write_list(url,method):
    '''
        判断访问的url是否在白名单(判断url+请求方式)
    '''
    url = ApiPermission.objects.filter(url=url,method=method)
    if url.exists():
        url_per = url.first().per_id.role.filter(name="白名单")
        if url_per.exists():
            return True
        return False
    return False
