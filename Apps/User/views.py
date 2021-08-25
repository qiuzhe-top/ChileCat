'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-24 19:29:44
Description: 用户模块
'''
import time

from Apps.User.utils import auth
from Apps.User.utils.exceptions import *
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from core.views import PermissionView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import request
from django.utils.translation import gettext_lazy as _
from rest_framework import fields

from . import models, serializers

site = ViewSite(name='User', app_name='User')


@site
class Login(CoolBFFAPIView):

    name = _('登录')
    response_info_serializer_class = serializers.TokenSerializer

    def get_context(self, request, *args, **kwargs):
        username = request.params.username
        password = request.params.password
        user = authenticate(username=username, password=password)
        if user is None:
            raise CoolAPIException(ErrorCode.ERR_USER_NOTFOUND)
        token = auth.update_token(user)
        return serializers.TokenSerializer(token, request=request).data

    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), max_length=25)),
            ('password', fields.CharField(label=_('密码'))),
        )

@site
class Logout(CoolBFFAPIView):

    name = _('退出登录')

    def get_context(self, request, *args, **kwargs):
      
        return None


@site
class Register(CoolBFFAPIView):

    name = _('注册')
    response_info_serializer_class = serializers.TokenSerializer

    def get_context(self, request, *args, **kwargs):
        username = request.params.username
        password = request.params.password
        password_repaet = request.params.password_repaet
        if password != password_repaet:
            raise CoolAPIException(ErrorCode.ERR_USER_DIFFERENT_PASSWORD)
        user, flg = User.objects.get_or_create(username=username)
        if not flg:
            raise CoolAPIException(ErrorCode.ERR_USER_DUPLICATE_USERNAME)
        user.set_password(password)
        user.save()
        token = auth.update_token(user)
        return serializers.TokenSerializer(token, request=request).data

    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), max_length=25)),
            ('password', fields.CharField(label=_('密码'))),
            ('password_repaet', fields.CharField(label=_('重复密码'))),
        )


@site
class Edit(CoolBFFAPIView):
    name = _('修改个人信息')


@site
class EditPassword(CoolBFFAPIView):
    name = _('修改密码')
    response_info_serializer_class = serializers.TokenSerializer

    def get_context(self, request, *args, **kwargs):
        password_old = request.params.password_old
        
        password_new = request.params.password_new
        password_new_repaet = request.params.password_new_repaet
        if password_new != password_new_repaet:
            raise CoolAPIException(ErrorCode.ERR_USER_DIFFERENT_PASSWORD)
        username = request.user.username
        if not authenticate(username=username, password=password_old):
            raise CoolAPIException(ErrorCode.ERR_USER_NO_PASSWORD)
        request.user.set_password(password_new)
        request.user.save()
        return None

    class Meta:
        param_fields = (
            ('password_old', fields.CharField(label=_('旧密码'), max_length=30)),
            ('password_new', fields.CharField(label=_('新密码'), max_length=30)),
            ('password_new_repaet', fields.CharField(label=_('重复新密码'), max_length=30)),
        )


@site
class Information(PermissionView):
    name = '获取个人信息 '
    response_info_serializer_class = serializers.UserInformationSerializer

    def get_context(self, request, *args, **kwargs):
        # time.sleep(1)
        return serializers.UserInformationSerializer(request.user, request=request).data


@site
class BindGrade(CoolBFFAPIView):
    name = '绑定班级'

    def get_context(self, request, *args, **kwargs):
        return 1

    class Meta:
        param_fields = (
            ('grade_id', fields.CharField(label=_('班级ID'))),

        )


# @site
# class Bindwechat(CoolBFFAPIView):
#     name = '绑定微信'

#     def get_context(self, request, *args, **kwargs):
#         js_code = self.__request.data['js_code']
#         username = self.__request.data['username']
#         password = self.__request.data['password']
#         if user:
#             __token = auth.update_token(user)
#         else:
#             return LoginExcept("用户不存在")
#         try:
#             tpost = OtherUser.objects.get(user=user)
#             old_openid = tpost.wx_openid
#         except OtherUser.DoesNotExist:
#             old_openid = None
#         if old_openid:
#             # print(old_openid)
#             raise VxBindException("请勿重新绑定")
#         openid = get_openid(js_code)
#         if openid is None:
#             raise VxBindException("微信用户异常")

#         tpost, b = OtherUser.objects.get_or_create(user=user)

#         if tpost.wx_openid:
#             return VxBindException("请勿重新绑定")
#         tpost.wx_openid = openid
#         tpost.save()
#         return -1

#     class Meta:
#         param_fields = (
#             'js_code',
#             fields.CharField(label=_('班级ID')),
#             'username',
#             fields.CharField(label=_('班级ID')),
#             'password',
#             fields.CharField(label=_('班级ID')),
#         )


def get_openid(js_code):
    """
    js_code : 微信客户端发送过来的标识
    根据js_code获取微信唯一标识
    """
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    data = {
        'appid': 'wx9a63d4bc0c3480f3',
        'secret': 'e8f66b9581ced527fb319c015e670044',
        'js_code': js_code,
    }
    ret = request.get(url, params=data)  # 发get请求
    try:
        openid = ret.json()['openid']
        return openid
    except KeyError:
        print('请检查 appid-secret 是否正确')
        return False


urls = site.urls
urlpatterns = site.urlpatterns
