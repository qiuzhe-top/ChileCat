'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-10 18:27:46
Description: 
'''

from Apps.User.utils.auth import get_groups
from cool import views
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from . import models

User = get_user_model()

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = ('id', 'name')


# class TeacherForGradeSerializer(serializers.ModelSerializer):
#     id = serializers.CharField(source='grade.id')
#     name = serializers.CharField(source='grade.name')

#     class Meta:
#         model = models.TeacherForGrade
#         fields = ('id', 'name')


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
        model = User
        fields = ('id', 'username')


class UserInformationSerializer(views.BaseSerializer):

    permissions = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    college = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()

    def get_experience(self,obj):
        return {'a':37,'b':100}

    def get_username(self,obj):
        try:
            return obj.name
        except:
            return obj.username
    
    def get_college(self,obj):
        try:
            return obj.grade.college.name
        except:
            return ''

    def get_grade(self, obj):
        try:
            return obj.grade.name
        except:
            return ''

    def get_avatar(self, obj):
        return 'https://s.pc.qq.com/tousu/img/20210823/4865226_1629724433.jpg'

    def get_roles(self, obj):
        return get_groups(obj)

    def get_permissions(self, obj):
        return obj.user_permissions.all().values_list('codename',flat=True)
    class Meta:
        model = User
        fields = (
            'username',
            'permissions',
            'roles',
            'grade',
            'college',
            'experience',
            'avatar',
            'is_staff',
            'is_superuser',
        )
