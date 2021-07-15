from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from Apps.SchoolInformation import models as SchoolInformationModels
from cool import views


from . import models


class TaskObtain(views.BaseSerializer):
    """获取任务"""

    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.college != None:
            return obj.college.name + " " + obj.get_types_display()
        else:
            return obj.get_types_display()
 
    class Meta:
        model = models.Task
        fields =('id','is_open','name')  # 包含

class TaskSwitch(views.BaseSerializer):
    """开启/关闭任务"""

    class Meta:
        model = models.Task
        fields =('is_open',)  # 包含




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
        fields = ('id', 'name', 'is_builder')  # 包含

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

class RecordQuery(serializers.ModelSerializer):
    '''考勤结果查询'''
    student_approved = serializers.CharField(source='student_approved.userinfo.name')
    student_approved_number = serializers.CharField(source='student_approved.username')
    # manager = serializers.CharField(source='manager.userinfo.name')
    worker = serializers.CharField(source='worker.userinfo.name')
    task = serializers.CharField(source = 'task.__str__')

    class Meta:

        model = models.Record
        # fields = ('id','task', 'rule_str','score','room_str','student_approved','student_approved_number','worker','score','star_time')  # 包含
        fields = "__all__"


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
    
# 晚查寝数据导出    
class TaskRecordExcelSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room_str')
    student_name = serializers.CharField(source='student_approved.userinfo.name')
    student = serializers.CharField(source='student_approved.username')
    reason = serializers.CharField(source='rule_str')
    classname = serializers.CharField(source='grade_str')
    created_time = serializers.CharField(source='star_time')

    class Meta:
        model =models.Record
        fields = ('created_time', 'room_name','classname','student','student_name','reason')  # 包含

class StudentDisciplinary(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room_str')
    student_name = serializers.CharField(source='student_approved.userinfo.name')
    student = serializers.CharField(source='student_approved.username')
    reason = serializers.CharField(source='rule_str')
    classname = serializers.CharField(source='grade_str')
    created_time = serializers.CharField(source='star_time')

    class Meta:
        model =models.Record
        fields = ('room_name', 'student','student_name','reason','classname','created_time')  # 包含