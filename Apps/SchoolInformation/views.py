'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-06 19:22:01
Description: 
'''
from Apps.SchoolInformation.models import StuInRoom
import json
import os
import re
import time

from Apps.SchoolAttendance import models
from Apps.User.models import StudentInfo, UserInfo
from cool.views import (
    CoolAPIException,
    CoolBFFAPIView,
    ErrorCode,
    ViewSite,
    param,
    utils,
)
from core.models_utils import search_room
from django.contrib.auth.models import Permission, User
from django.core.checks import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from openpyxl.reader.excel import load_workbook
from rest_framework import fields
from rest_framework.views import APIView
from Apps.SchoolAttendance import serializers as attendance_serializers
from . import serializers
from core.views import PermissionView
# Create your views here.

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
        room = StuInRoom.objects.get(user=request.user).room
        rooms = StuInRoom.objects.filter(room=room)
        return attendance_serializers.DormStudentRoomInfoTrue(rooms, many=True, request=request).data

urls = site.urls
urlpatterns = site.urlpatterns
