'''
Author: 邹洋
Date: 2022-01-12 21:14:49
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 16:41:56
Description: 
'''
from cool import views
from django.contrib.auth import get_user_model
from rest_framework import serializers

from AppUser.common.auth import get_groups

from . import models

User = get_user_model()


class TokenSerializer(views.BaseSerializer):
    class Meta:
        model = models.Token
        fields = ('token',)


class UserInformationBaseSerializer(views.BaseSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        if obj.username:
            return obj.username
        else:
            return obj.name
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'name',
            'tel'
        )


class UserInformationSerializer(views.BaseSerializer):

    permissions = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()

    def get_experience(self, obj):
        return {'a': 37, 'b': 100}

    def get_name(self, obj):
        if obj.name:
            return obj.name
        else:
            return obj.username

    def get_avatar(self, obj):
        return 'https://s.pc.qq.com/tousu/img/20210823/4865226_1629724433.jpg'

    def get_roles(self, obj):
        return get_groups(obj)

    def get_permissions(self, obj):
        return obj.user_permissions.all().values_list('codename', flat=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'name',
            'permissions',
            'roles',
            'gender',
            'tel',
            'email',
            'home_address',
            'photo',
            'experience',
            'avatar',
            'is_staff',
            'is_superuser',
        )
