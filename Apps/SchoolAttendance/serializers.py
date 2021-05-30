from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from Apps.SchoolInformation import models as SchoolInformationModels

from . import models


class TaskAdmin(serializers.ModelSerializer):
    """审批记录序列化"""

    name = serializers.SerializerMethodField()
    id = serializers.IntegerField(source="task.id")
    is_open = serializers.BooleanField(source="task.is_open")
    is_builder = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.task.college.name + " " + obj.task.get_types_display()

    def get_is_builder(self, obj):
        return obj.task.user == obj.user

    class Meta:
        model = models.TaskPlayer
        fields = ('id', 'is_open', 'name', 'is_builder')  # 包含


class TaskBuilder(serializers.ModelSerializer):
    """审批记录序列化"""

    name = serializers.SerializerMethodField()
    is_builder = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.college.name + " " + obj.get_types_display()

    def get_is_builder(self, obj):
        return True

    class Meta:
        model = models.Task
        fields = ('id', 'is_open', 'name', 'is_builder')  # 包含

class TaskPlayerGetAdmin(serializers.ModelSerializer):
    """获取任务关联管理员"""
    user_id = serializers.IntegerField(source="user.id")
    uese_name = serializers.CharField(source="user.username")

    class Meta:
        model = models.TaskPlayer
        fields = ('user_id', 'uese_name')  # 包含

class TaskExecutor(serializers.ModelSerializer):
    """执行人获取任务"""
    builder_name = serializers.CharField(source="task.user.userinfo.name")
    id = serializers.CharField(source="task.id")
    title = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.task.get_types_display() + "-" + obj.task.college.name

    def get_type(self, obj):
        return obj.task.types

    class Meta:
        model = models.TaskPlayer
        fields = ('id', 'title','builder_name','is_finish','type')  # 包含

class ConditionRecord(serializers.ModelSerializer):
    '''获取考勤执行记录 晚查寝 晚自修'''
    student_approved = serializers.CharField(source='student_approved.userinfo.name')
    student_approved_number = serializers.CharField(source='student_approved.username')
    worker = serializers.CharField(source='worker.userinfo.name')
    class Meta:
        model = models.Record
        fields = ('id', 'rule_str','room_str','student_approved','student_approved_number','worker','score','star_time')  # 包含


class UserCallGrader(serializers.ModelSerializer):
    name = serializers.CharField(source='userinfo.name')
    # flg = serializers.CharField(source='usercall_set.flg')
    flg = serializers.SerializerMethodField()
    def get_flg(self,obj):
        call = obj.user_call
        print(call)
        if call:
            return call.flg
        return call

    class Meta:
        model =User
        fields = ('id', 'name','username','flg')  # 包含
