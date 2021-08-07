'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors: Please set LastEditors
LastEditTime: 2021-08-01 13:25:48
Description: 
'''

from Apps.User.utils.auth import get_groups
from cool import views
from cool.views import view
from django.contrib.contenttypes.models import ContentType
from rest_framework import fields, serializers

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
        fields = ('id', 'username')


class UserInformationSerializer(views.BaseSerializer):

    permissions = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    

    def get_username(self,obj):
        try:
            return obj.userinfo.name
        except:
            return obj.username
            
    def get_grade(self, obj):
        st = models.StudentInfo.objects.filter(user=obj)
        if st.exists():
            return st[0].grade.name
        else:
            return '该用户无班级'

    def get_avatar(self, obj):
        return 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'

    def get_roles(self, obj):
        return get_groups(obj)

    def get_permissions(self, obj):
        return obj.user_permissions.all().values_list('codename',flat=True)
    class Meta:
        model = models.User
        fields = (
            'username',
            'permissions',
            'roles',
            'grade',
            'avatar',
            'is_staff',
            'is_superuser',
        )