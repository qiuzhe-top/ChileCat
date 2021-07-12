'''
Author: 邹洋
Date: 2021-07-11 15:27:50
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-11 15:52:55
Description: 
'''
from rest_framework import serializers

from rest_framework.fields import CharField
from . import models

from cool import views


class UserSerializer(views.BaseSerializer):
    name = serializers.CharField(source='userinfo.name')
    tel = serializers.CharField(source='userinfo.tel')
    grade = serializers.CharField(source='userinfo.grade.name')
    class Meta:
        model = models.User
        fields = ('id', 'username','name','grade','tel')
