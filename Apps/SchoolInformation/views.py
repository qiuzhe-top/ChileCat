'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-10 18:27:16
Description: 
'''
from Apps.SchoolAttendance import models
from Apps.SchoolAttendance import serializers as attendance_serializers
from Apps.SchoolInformation.models import StuInRoom
from cool.views import CoolAPIException, ErrorCode, ViewSite
from core.views import PermissionView
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
        in_room = StuInRoom.objects.get(user=request.user)
        bed = StuInRoom.objects.filter(room=in_room.room,bed_position=position)
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
        d =  models.College.objects.all().values('id','name')
        return list(d)
        
urls = site.urls
urlpatterns = site.urlpatterns
