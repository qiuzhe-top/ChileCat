'''
Author: 邹洋
Date: 2021-07-11 15:27:50
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-20 09:46:20
Description: 
'''
from cool import views
from rest_framework import serializers

from . import models


class UserSerializer(views.BaseSerializer):
    name = serializers.CharField(source='userinfo.name')
    tel = serializers.CharField(source='userinfo.tel')
    grade = serializers.CharField(source='studentinfo.grade.name')
    class Meta:
        model = models.User
        fields = ('id', 'username','name','grade','tel')
