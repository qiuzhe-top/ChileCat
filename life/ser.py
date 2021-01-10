'''序列化取出表内数据'''
from rest_framework import serializers
from .models import TaskRecord

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
        fields = ('classname','roomname','stuid','stuname','reason','workername','createdtime')
