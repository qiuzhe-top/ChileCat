"""序列化取出表内数据"""
from rest_framework import serializers
from .models import TaskRecord
import datetime


class TaskRecordSerializer(serializers.ModelSerializer):
    """查寝记录数据的序列化"""
    classname = serializers.CharField(source='student_approved.studentinfo.grade.name')
    room_name = serializers.SerializerMethodField()
    student = serializers.CharField(source='student_approved.user_name')
    student_name = serializers.CharField(source='student_approved.userinfo.name')
    worker_name = serializers.CharField(source='worker.userinfo.name')

    def get_room_name(self, value):
        """自定义寝室号格式"""
        return value.building.name + "-" + value.room.floor.name + value.room.name

    class Meta:
        model = TaskRecord
        fields = ('id', 'classname', 'room_name', 'student', 'student_name', 'reason', 'worker_name', 'created_time')


class TaskRecordAntiSerializer(serializers.ModelSerializer):
    """查寝记录反序列化"""
    # TODO 查寝记录反向序列化
    def create(self, validated_data):

        return TaskRecord.objects.create(**validated_data)


class TaskRecordExcelSerializer(TaskRecordSerializer):
    """查寝记录数据输出excel的序列化"""
    date = serializers.SerializerMethodField()
    classname = serializers.CharField(source='student_approved.studentinfo.grade.name')

    def get_date(self, value):
        """显示日期而不是时间"""
        return value.created_time.date().strftime("%Y-%m-%d")

    class Meta:
        model = TaskRecord
        fields = ('date', 'room_name', 'classname', 'student', 'student_name', 'reason')
