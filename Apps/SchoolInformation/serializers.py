'''
Author: 邹洋
Date: 2021-07-11 15:27:50
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-09 18:48:08
Description: 
'''
from cool import views
from rest_framework import serializers

from django.conf import settings
User = settings.AUTH_USER_MODEL

class UserSerializer(views.BaseSerializer):
    tel = serializers.CharField(source='tel')
    grade = serializers.CharField(source='grade.name')
    class Meta:
        model = User
        fields = ('id', 'username','name','grade','tel')
