'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-24 15:47:03
Description: 
'''
from cool.views.view import CoolBFFAPIView
from Apps.SchoolAttendance.models import *
from Apps.SchoolAttendance import serializers as attendance_serializers
from Apps.SchoolInformation.models import StuInRoom
from cool.views import CoolAPIException, ErrorCode, ViewSite
from core.views import PermissionView, TaskBase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import fields

from . import serializers

User = get_user_model()
site = ViewSite(name='SchoolInformation', app_name='SchoolInformation')


 
@site
class StudentInformation(PermissionView):

    name = _('考勤 获取用户基本信息')
    response_info_serializer_class = serializers.UserSerializer

    def get_context(self, request, *args, **kwargs):
        username = request.params.username
        user = User.objects.filter(username=username)
        if not user.exists():
            raise CoolAPIException(ErrorCode.ERR_USER_UNABLE_TO_SEARCH_FOR_USERR)
        return serializers.UserSerializer(user[0], request=request).data

    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), max_length=25)),
        )
@site
class UpdateBeds(PermissionView):
    name = _('修改床位')
    def get_context(self, request, *args, **kwargs):
        position = request.params.position
        in_room = StuInRoom.objects.get(user=request.user) # 我的床位
        bed = StuInRoom.objects.filter(room=in_room.room,bed_position=position) # 他人的床位
        if bed.exists():
            bed = bed[0]
            bed.bed_position = in_room.bed_position
            bed.save()
        in_room.bed_position=position
        in_room.save()
    class Meta:
        param_fields = (
            ('position',fields.IntegerField(label=_('床位'))),
        )
@site
class Mybedroom(PermissionView):
    name = _('我的寝室信息')
    response_info_serializer_class = attendance_serializers.DormStudentRoomInfoTrue
   
    def get_context(self, request, *args, **kwargs):
        try:
            room = StuInRoom.objects.get(user=request.user).room
        except:
            raise CoolAPIException(ErrorCode.DORMITORY_NOT_ARRANGED)
        rooms = StuInRoom.objects.filter(room=room)
        return attendance_serializers.DormStudentRoomInfoTrue(rooms, many=True, request=request).data
@site
class CollegeQuery(PermissionView):
    name = _('获取分院')
    
    def get_context(self, request, *args, **kwargs):
        d =  College.objects.all().values('id','name')
        return list(d)

@site
class StuRoomDelete(PermissionView):
    name = _('寝室入住 软删除')
   
    def get_context(self, request, *args, **kwargs):
        #TODO 无法区分分院
        username_list = request.params.username_list
        return StuInRoom.objects.filter(user__username__in=username_list,is_active=False).update(is_active=False)

    class Meta:
        param_fields = (
            ('username_list', fields.ListField(label=_('用户名列表'), default=None)),
        )
@site
class StuRoomRecover(PermissionView):
    name = _('寝室入住 恢复')
   
    def get_context(self, request, *args, **kwargs):
        username_list = request.params.username_list
        task_id = int(request.params.task_id)
        if request.params.is_all:
            # 获取任务对应的楼层进行恢复
            rooms = Task.objects.filter(id=task_id,admin=request.user).values_list('buildings__floor__room',flat=True)  
            return StuInRoom.objects.filter(room__in=rooms,is_active=False).update(is_active=True)
        else:
            return StuInRoom.objects.filter(user__username__in=username_list,is_active=False).update(is_active=True)
    class Meta:
        param_fields = (
            ('username_list', fields.ListField(label=_('用户名列表'), default=None)),
            ('is_all', fields.BooleanField(label=_('是否全部恢复'))),
            ('task_id', fields.CharField(label=_('任务id'))),
        )
urls = site.urls
urlpatterns = site.urlpatterns
