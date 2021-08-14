from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from Apps.SchoolInformation import models as SchoolInformationModels
from cool import views
import time

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


class TimeSerializer(views.BaseSerializer):
    star_time = serializers.SerializerMethodField()
    last_time = serializers.SerializerMethodField()
    def get_star_time(self,obj):
        t  = obj.star_time
        day = t.day
        month = t.month
        year = t.year
        hour = t.hour
        minute = t.minute
        return '{}-{}-{} {}:{}'.format(year,month,day,hour,minute)
    def get_last_time(self,obj):
        t  = obj.last_time
        day = t.day
        month = t.month
        year = t.year
        hour = t.hour
        minute = t.minute
        return '{}-{}-{} {}:{}'.format(year,month,day,hour,minute)
class PersonalDisciplineQuery(TimeSerializer,views.BaseSerializer):
    '''获取个人违纪记录'''
    worker = serializers.CharField(source='worker.userinfo.name')

    class Meta:
        model = models.Record
        fields =('rule_str','score','worker','star_time')  
class DormRoomInfo(views.BaseSerializer):
    '''层内房间列表'''
    status = serializers.SerializerMethodField()

    def get_status(self,obj):
        task = self.request.task
        history = models.RoomHistory.objects.get_or_create(task=task, room=obj)[0]
        if task.types == '0':
            return history.is_knowing
        elif task.types == '1':
            return history.is_health
          
    class Meta:
        model = models.Room
        fields =('id', 'name', 'status')  

class DormStudentRoomInfo(views.BaseSerializer):
    '''晚查寝-宿舍房间 数据'''
    name = serializers.CharField(source='user.userinfo.name')
    id = serializers.IntegerField(source='user.id')
    status = serializers.SerializerMethodField()
    
    def get_status(self, obj):
        task = self.request.task
        if task.types == '1':
            return True
        status, flg = models.TaskFloorStudent.objects.get_or_create(task=task, user=obj.user)
        return status.flg
    
    class Meta:
        model = models.StuInRoom
        fields =('id','name','bed_position','status')  
class DormStudentRoomInfoTrue(DormStudentRoomInfo):
    def get_status(self, obj):
        return True
class TaskSwitch(views.BaseSerializer):
    """开启/关闭任务"""

    class Meta:
        model = models.Task
        fields =('is_open',)  # 包含



class UserCallSerializer(views.BaseSerializer):
    """任务点名 -- 学生"""
    name = serializers.CharField(source="user.userinfo.name")
    username = serializers.CharField(source="user.username")
    user_id = serializers.SerializerMethodField()

    def get_user_id(self,obj):
        return obj.user.id
    class Meta:
        model = models.UserCall
        fields = ('user_id','username','name','flg')  # 包含

class TaskExecutor(views.BaseSerializer):
    """执行人获取任务"""
    # builder_name = serializers.CharField(source="task.user.userinfo.name")
    id = serializers.CharField(source="task.id")
    title = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_title(self, obj):
        # return obj.task.get_types_display() + "-" + obj.task.college.name
        return obj.task.get_name()

    def get_type(self, obj):
        return obj.task.types

    class Meta:
        model = models.TaskPlayer
        fields = ('id', 'title','is_finish','type')  # 包含


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

class RecordUserInfo(views.BaseSerializer):
    student_approved = serializers.SerializerMethodField()
    student_approved_number = serializers.SerializerMethodField()

    def get_student_approved(self,obj):
        try:
            return obj.student_approved.userinfo.name
        except:
            return None
    def get_student_approved_number(self,obj):
        try:
            return obj.student_approved.username
        except:
            return None
class RecordQuery(RecordUserInfo,TimeSerializer):
    '''考勤结果查询'''
    worker = serializers.CharField(source='worker.userinfo.name')
    task = serializers.CharField(source = 'task.__str__')
    class Meta:

        model = models.Record
        fields = ('id','task', 'rule_str','score','room_str','grade_str','student_approved','student_approved_number','worker','score','star_time')  # 包含


class ConditionRecord(TimeSerializer,RecordUserInfo):
    '''获取考勤执行记录 晚查寝 晚自修'''
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
    
class TaskRecordExcelSerializer(serializers.ModelSerializer):
    '''晚查寝数据导出'''    
    room_name = serializers.CharField(source='room_str')
    student_name = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    reason = serializers.CharField(source='rule_str')
    classname = serializers.CharField(source='grade_str')
    created_time = serializers.CharField(source='star_time')
    def get_student_name(self,obj):
        try:
            return obj.student_approved.userinfo.name
        except:
            return None
    def get_student(self,obj):
        try:
            return obj.student_approved.username
        except:
            return None
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


