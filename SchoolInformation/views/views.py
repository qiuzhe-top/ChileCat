# '''
# Author: 邹洋
# Date: 2022-01-11 19:44:42
# Email: 2810201146@qq.com
# LastEditors:  
# LastEditTime: 2022-02-07 10:45:04
# Description: 
# '''
# '''
# Author: 邹洋
# Date: 2021-05-20 08:37:12
# Email: 2810201146@qq.com
# LastEditors:  
# LastEditTime: 2022-02-07 10:25:18
# Description: 
# '''
# from cool.views.view import CoolBFFAPIView
# from Apps.SchoolAttendance.models import *
# from Apps.SchoolAttendance import serializers as attendance_serializers
# from Apps.SchoolInformation.models import StuInRoom
# from cool.views import CoolAPIException, ErrorCode, ViewSite
# from Core.views import PermissionView, TaskBase
# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
# from rest_framework import fields

# from .. import serializers

# User = get_user_model()
# site = ViewSite(name='SchoolInformation', app_name='SchoolInformation')


 
# @site
# class StudentInformation(PermissionView):

#     name = _('考勤 获取用户基本信息')
#     response_info_serializer_class = serializers.UserSerializer

#     def get_context(self, request, *args, **kwargs):
#         username = request.params.username
#         user = User.objects.filter(username=username)
#         if not user.exists():
#             raise CoolAPIException(ErrorCode.ERR_USER_UNABLE_TO_SEARCH_FOR_USERR)
#         return serializers.UserSerializer(user[0], request=request).data

#     class Meta:
#         param_fields = (
#             ('username', fields.CharField(label=_('用户名'), max_length=25)),
#         )

# @site
# class CollegeQuery(PermissionView):
#     name = _('获取分院')
    
#     def get_context(self, request, *args, **kwargs):
#         d =  College.objects.all().values('id','name')
#         return list(d)

# from .dormitory import urlpatterns_dormitory
# urls = site.urls
# urlpatterns = site.urlpatterns + urlpatterns_dormitory
