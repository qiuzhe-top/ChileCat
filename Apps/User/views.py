'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-10 14:45:47
Description: 用户模块
'''
from Apps.User.models import StudentInfo, TeacherForGrade
from Apps.User.utils import auth
from Apps.User.utils.exceptions import *
from Apps.User.utils.user import UserExtraOperate
from cool.views import (
    CoolAPIException,
    CoolBFFAPIView,
    ErrorCode,
    ViewSite,
    param,
    utils,
)
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from Manage.models_extension.models_permission import ApiPermission
from rest_framework import fields
from rest_framework.views import APIView

from . import models, serializers
from .utils.auth import get_groups

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
            raise CoolAPIException(ErrorCode.ERR_DEMO_NOTFOUND)
        token = auth.update_token(user)
        return serializers.TokenSerializer(token, request=request).data

    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), max_length=25)),
            ('password', fields.CharField(label=_('密码'))),
        )


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


# @site
# class Edit(CoolBFFAPIView):
#     name = _('修改个人信息')


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
        if not authenticate(username=username,password=password_old):
            raise CoolAPIException(ErrorCode.ERR_USER_NO_PASSWORD)
        request.user.set_password(password_new)
        request.user.save()        
        return None
    class Meta:
        param_fields = (
            ('password_old', fields.CharField(label=_('旧密码'),max_length=30)),
            ('password_new', fields.CharField(label=_('新密码'),max_length=30)),
            ('password_new_repaet', fields.CharField(label=_('重复新密码'),max_length=30)),
        )
@site    
class Information(CoolBFFAPIView):
    name = '获取个人信息 '
    response_info_serializer_class = serializers.UserInformationSerializer
class Information(APIView):
    '''获取个人信息'''

    API_PERMISSIONS = ['获取个人信息', '*get']
    '''
    Information
    '''

    def get(self, request):
        '''
        get method
        获取用户
        获取用户信息
        返回信息
        '''
        ret = {'code': 2000, 'message': '执行成功', 'data': {}}
        user = self.request.user
        data = {'permissions': []}

        p = (
            self.request.user.user_permissions.filter()
            .exclude(content_type=ContentType.objects.get_for_model(ApiPermission))
            .values()
        )

        # TODO 模型发生变化 operatepermission 失效
        for permission in p:
            if 'operatepermission' not in permission['codename']:
                data['permissions'].append(permission['codename'])

        data['roles'] = get_groups(request)
        data['introduction'] = 'I am a super administrator'
        data[
            'avatar'
        ] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'

        try:
            data['name'] = user.userinfo.name
        except:
            ret['code'] = 5000
            ret['message'] = '用户信息不完整'
            return JsonResponse(ret)

        data['is_admin'] = request.user.is_staff
        data['is_superuser'] = request.user.is_superuser
        try:
            data['grade'] = (
                StudentInfo.objects.get(user=self.request.user).grade.name
                if StudentInfo.objects.filter(user=self.request.user).exists()
                else '该用户无班级'
            )
            ret['data'] = data
        except StudentInfo.DoesNotExist:
            data['grade'] = ''
        return JsonResponse(ret)


class ClassList(APIView):
    '''关联班级'''

    API_PERMISSIONS = ['关联班级', '*get']

    def get(self, request):
        '''关联班级'''
        ret = {}
        user = self.request.user

        try:
            info = user.userinfo
        except:
            ret['code'] = 5000
            ret['message'] = '用户信息不完整'
            return JsonResponse(ret)

        try:
            ser_list = ''
            if info.identity == 'student':
                grade = user.studentinfo.grade
                # django 序列化
                ser_list = serializers.GradeSerializer(instance=grade, many=False).data
            elif info.identity == 'teacher':
                grade = TeacherForGrade.objects.filter(user_id=self.request.user)
                ser_list = serializers.TeacherForGradeSerializer(
                    instance=grade, many=True
                ).data
            elif info.identity == 'college':
                college_list = userializers.Teacherforcollege_set.all()
                ser_list = serializers.TeacherForCollegeSerializer(
                    instance=college_list, many=True
                ).data
                ser_all_class = []
                for item in ser_list:
                    for k, v in item.items():
                        ser_all_class += v
                ser_list = ser_all_class
            if len(ser_list) == 0:
                ret['code'] = 5000
                ret['message'] = '您的班级未绑定，请联系管理员'
                return JsonResponse(ret)
            ret['code'] = 2000
            ret['message'] = '执行成功'
            ret['data'] = ser_list
        except:
            ret['code'] = 5000
            ret['message'] = '未知班级信息'
            ret['data'] = ser_list
        return JsonResponse(ret)


# 绑定微信
class BindVx(APIView):
    '''
    绑定微信
    '''

    API_PERMISSIONS = ['绑定微信', '*post']

    def post(self, request):
        '''
        微信绑定
        '''
        ret = {'code': 0000, 'message': '', 'data': {'token': ''}}
        try:
            print('绑定微信界面')
            ret['data']['token'] = UserExtraOperate(self.request).vx_bind()
            ret['code'] = 2000
            ret['message'] = '绑定成功'
        except VxBindException as bind_failed:
            ret['code'] = 5000
            ret['message'] = str(bind_failed)
        return JsonResponse(ret)


urls = site.urls
urlpatterns = site.urlpatterns
