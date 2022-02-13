from cool import views
from django.contrib.auth import get_user_model
from rest_framework import serializers

from AppInformation.models import StuInRoom

from . import models

User = get_user_model()

class TaskObtain(views.BaseSerializer):
    """获取任务"""

    name = serializers.SerializerMethodField()
    buildings = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_name()
        
    def get_buildings(self, obj):
        return obj.get_buildings()
 
    class Meta:
        model = models.Task
        fields =('id','is_open','name','buildings')  # 包含



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
    
    worker = serializers.CharField(source='worker_name')
    student_approved = serializers.SerializerMethodField()

    def get_student_approved(self,obj):
        try:
            return obj.student_approved_name
        except:
            return '寝室'
    class Meta:
        model = models.Record
        fields =('rule_str','score','worker','student_approved','star_time')  

class DormStudentRoomInfoTrue(views.BaseSerializer):
    '''晚查寝-宿舍房间 数据'''
    name = serializers.CharField(source='user.name')
    user_id = serializers.CharField(source='user.username')
    id = serializers.CharField(source='user.username')
    status = serializers.SerializerMethodField()
    
    def get_status(self, obj):
        return '0'
    
    class Meta:
        model = models.StuInRoom
        fields =('user_id','id', 'name','bed_position','status')  

class TaskSwitch(views.BaseSerializer):
    """开启/关闭任务"""

    class Meta:
        model = models.Task
        fields =('is_open',)  # 包含



# class UserCallSerializer(views.BaseSerializer):
#     """任务点名 -- 学生"""
#     name = serializers.CharField(source="user.name")
#     username = serializers.CharField(source="user.username")
#     user_id = serializers.SerializerMethodField()

#     def get_user_id(self,obj):
#         return obj.user.id
#     class Meta:
#         model = models.UserCall
#         fields = ('user_id','username','name','flg')  # 包含

class TaskExecutor(views.BaseSerializer):
    """执行人获取任务"""
    # builder_name = serializers.CharField(source="task.user.userinfo.name")
    title = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    grades = serializers.SerializerMethodField()
    buildings = serializers.SerializerMethodField()

    def get_grades(self, obj):
        return obj.get_grades()

    def get_buildings(self, obj):
        return obj.get_buildings()


    def get_title(self, obj):
        return obj.get_name()

    def get_type(self, obj):
        return obj.types

    class Meta:
        model = models.Task
        fields = ('id', 'title','buildings','grades','type')  # 包含


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

# class TaskPlayerGetAdmin(serializers.ModelSerializer):
#     """获取任务关联管理员"""
#     user_id = serializers.IntegerField(source="user.id")
#     uese_name = serializers.CharField(source="user.username")

#     class Meta:
#         model = models.TaskPlayer
        fields = ('user_id', 'uese_name')  # 包含

class RecordUserInfo(views.BaseSerializer):
    student_approved = serializers.SerializerMethodField()
    student_approved_number = serializers.SerializerMethodField()

    def get_student_approved(self,obj):
        try:
            return obj.student_approved_name
        except:
            return None
    def get_student_approved_number(self,obj):
        try:
            return obj.student_approved_username
        except:
            return None
class RecordQuery(RecordUserInfo,TimeSerializer):
    '''考勤结果查询'''
    worker = serializers.CharField(source='worker_name')
    task = serializers.CharField(source = 'task.__str__')
    worker = serializers.CharField(source='worker_name')
    student_approved = serializers.CharField(source='student_approved_name')

    class Meta:

        model = models.Record
        fields = ('id','task', 'rule_str','score','score','room_str','grade_str','student_approved','student_approved_number','worker','score','star_time')  # 包含


class ConditionRecord(TimeSerializer,RecordUserInfo):
    '''获取考勤执行记录 晚查寝 晚自修'''
    worker = serializers.CharField(source='worker_name')
    student_approved = serializers.CharField(source='student_approved_name')

    class Meta:
        model = models.Record
        fields = ('id', 'rule_str','room_str','student_approved','student_approved_number','worker','score','star_time')  # 包含


# class UserCallGrader(serializers.ModelSerializer):
#     flg = serializers.SerializerMethodField()
#     def get_flg(self,obj):
#         call = obj.user_call
#         if call:
#             return call.flg
#         return call

#     class Meta:
#         model =User
#         fields = ('id', 'name','username','flg')  # 包含
    
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
            return obj.student_approved_name
        except:
            return None
    def get_student(self,obj):
        try:
            return obj.student_approved_username
        except:
            return None
    class Meta:
        model =models.Record
        fields = ('created_time', 'room_name','classname','student','student_name','reason','score')  # 包含

class StudentDisciplinary(views.BaseSerializer):
    room_name = serializers.CharField(source='room_str')
    student_name = serializers.CharField(source='student_approved_name')
    student = serializers.CharField(source='student_approved_username')
    reason = serializers.CharField(source='rule_str')
    classname = serializers.CharField(source='grade_str')
    created_time = serializers.CharField(source='star_time')

    class Meta:
        model =models.Record
        fields = ('room_name', 'student','student_name','reason','classname','created_time')  # 包含


