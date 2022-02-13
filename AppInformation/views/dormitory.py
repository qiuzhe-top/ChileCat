'''
Author: 邹洋
Date: 2022-02-06 22:15:24
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-12 21:40:01
Description: 学校宿舍
'''
import json
from AppInformation.models import *
from AppAttendance.models import Task
from Core.views import PermissionView
from rest_framework import fields
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from AppAttendance import serializers as attendance_serializers
from django.utils.translation import gettext_lazy as _
site = ViewSite(name='AppInformation', app_name='AppInformation')

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
            rooms = Task.objects.filter(id=task_id,admin=request.user).values_list('buildings',flat=True)  
            rooms = json.loads(rooms[0])
            return StuInRoom.objects.filter(room_id__in=rooms,is_active=False).update(is_active=True)
        else:
            return StuInRoom.objects.filter(user__username__in=username_list,is_active=False).update(is_active=True)
    class Meta:
        param_fields = (
            ('username_list', fields.ListField(label=_('用户名列表'), default=None)),
            ('is_all', fields.BooleanField(label=_('是否全部恢复'))),
            ('task_id', fields.CharField(label=_('任务id'))),
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


urls_dormitory = site.urls
urlpatterns_dormitory = site.urlpatterns
