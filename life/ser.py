'''序列化取出表内数据'''
from rest_framework import serializers
from .models import TaskRecord
import datetime
class TaskTecordSerializer(serializers.ModelSerializer):
    '''查寝记录数据的序列化'''
    classname = serializers.CharField(source='objstuid.studentinfo.grade_id.name')
    roomname = serializers.SerializerMethodField()
    stuid = serializers.CharField(source='objstuid.user_name')
    stuname = serializers.CharField(source='objstuid.userinfo.name')
    workername = serializers.CharField(source='workerid.userinfo.name')

    def get_roomname(self,value):
        '''自定义寝室号格式'''
        return value.buildingid.budnum + "-" + value.roomid.floor.floornum + value.roomid.roomnum
    class Meta:
        model = TaskRecord
        fields = ('id','classname','roomname','stuid','stuname','reason','workername','createdtime')

class TaskTecordSerializer1(serializers.ModelSerializer):
    '''查寝记录数据输出excel的序列化'''
    #date = serializers.DateField(source='createdtime')
    date = serializers.SerializerMethodField()
    roomname = serializers.SerializerMethodField()
    classname = serializers.CharField(source='objstuid.studentinfo.grade_id.name')
    stuid = serializers.CharField(source='objstuid.user_name')
    stuname = serializers.CharField(source='objstuid.userinfo.name')
    def get_roomname(self,value):
        '''自定义寝室号格式'''
        return value.buildingid.budnum + "-" + value.roomid.floor.floornum + value.roomid.roomnum
    def get_date(self,value):
        '''显示日期而不是时间'''
        return value.createdtime.date().strftime("%Y-%m-%d")
    class Meta:
        model = TaskRecord
        fields = ('date','roomname','classname','stuid','stuname','reason')
