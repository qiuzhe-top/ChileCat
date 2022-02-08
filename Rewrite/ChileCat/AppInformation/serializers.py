'''
Author: 邹洋
Date: 2021-07-11 15:27:50
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 17:23:41
Description: 
'''
from cool import views
from rest_framework import serializers


from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(views.BaseSerializer):
    grade = serializers.CharField(source='grade.id')
    class Meta:
        model = User
        fields = ('id', 'username','name','grade','tel')
