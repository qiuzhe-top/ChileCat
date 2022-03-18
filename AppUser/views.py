import imp
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from rest_framework import fields
from core.common.excel import ExcelBase

from core.views import PermissionView

from .common.auth import update_token
from . import serializers
from .common.configuration import *
from .models import *
User = get_user_model()

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
        token = update_token(user)
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
        token = update_token(user)
        return serializers.TokenSerializer(token, request=request).data

    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), max_length=25)),
            ('password', fields.CharField(label=_('密码'))),
            ('password_repaet', fields.CharField(label=_('重复密码'))),
        )

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
    name = '获取个人信息'
    response_info_serializer_class = serializers.UserInformationSerializer

    def get_context(self, request, *args, **kwargs):
        return serializers.UserInformationSerializer(request.user, request=request).data


@site
class GetUserManage(CoolBFFAPIView):
    name = _('通过账号获取用户')
    response_info_serializer_class = serializers.UserInformationSerializer
    
    def get_by_username(self,request):
        try:
            user = User.objects.get(username = request.params.username)
            data = serializers.UserInformationBaseSerializer(user, request=request).data
            return data
        except:
            raise CoolAPIException(ErrorCode.ERR_USER_UNABLE_TO_SEARCH_FOR_USERR)
            
    def fileter_user_by_username(self,request):
        user = User.objects.filter(username__in = request.params.username_list)
        return serializers.UserInformationBaseSerializer(user,many=True, request=request).data 

    def get_context(self, request, *args, **kwargs):
        fun = {}
        fun['get_by_username'] = self.get_by_username
        fun['fileter_user_by_username'] = self.fileter_user_by_username
        return fun[request.params.type](request)
            

    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), default=None)),
            ('username_list', fields.ListField(label=_('用户名列表'), default=None)),
            ('type', fields.CharField(label=_('查询类型'))),
        )
@site
class SimpleCreateUser(PermissionView):
    name = _('简单创建用户')
   
    def get_context(self, request, *args, **kwargs):
        mode_users = []
        username_simple_dict = request.params.username_simple_dict
        usernames = username_simple_dict.keys()
        db_usernames = User.objects.filter(username__in=usernames).values_list('username',flat=True)
        # 循环数据库没有的账号
        for username in set(usernames) - set(db_usernames):
            name = username_simple_dict[username]
            value = {"username":username,"name":name,"password":PASSWOED_123456}
            mode_users.append(User(**value))
        User.objects.bulk_create(mode_users)
            

    class Meta:
        param_fields = (
            ('username_simple_dict', fields.DictField(label=_('用户名姓名字典'), default={})),
        )
@site
class Logout(CoolBFFAPIView):

    name = _('退出登录')

    def get_context(self, request, *args, **kwargs):

        return None

# @site
class UpdatePassword(CoolBFFAPIView,ExcelBase):
    name = _('批量修改密码')
   
    def get_context(self, request, *args, **kwargs):
        data = []
        users = self.excel_to_list(request)
        for user in users:
            n = user['username']
            p = user['password']
            if PASSWOED_123456 != p:
                data.append(user)

        for user in data:
            n = user['username']
            p = user['password']
            User.objects.filter(username=n).update(password=p)


urls = site.urls
urlpatterns = site.urlpatterns
