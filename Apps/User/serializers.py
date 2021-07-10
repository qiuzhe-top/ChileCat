'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-10 14:46:43
Description: 
'''

from cool.views import view
from . import models
from rest_framework import fields, serializers
from cool import views
from rest_framework import serializers

from . import models
from .backend import BaseUserBackend


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = ('id', 'name')


class TeacherForGradeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='grade.id')
    name = serializers.CharField(source='grade.name')

    class Meta:
        model = models.TeacherForGrade
        fields = ('id', 'name')


class TeacherForCollegeSerializer(serializers.ModelSerializer):
    listGrader = serializers.SerializerMethodField()

    class Meta:
        model = models.TeacherForCollege
        fields = ('listGrader',)  # 包含

    def get_listGrader(self, obj):
        d = obj.college.grade_set.all()
        ser = GradeSerializer(instance=d, many=True).data
        ret = []
        for item in ser:
            dicts = {}
            for k, v in item.items():
                dicts[k] = v
            ret.append(dicts)
        return ret


class TokenSerializer(views.BaseSerializer):
    class Meta:
        model = models.Token
        fields = ('token',)


class UserSerializer(views.BaseSerializer):
    class Meta:
        model = models.User
        fields = ('id','username')

class UserInformationSerializer(views.BaseSerializer):
    class Meta:
        models = models.User
        fields =   ('id','username')