"""暂时不写反向序列化"""
import datetime
from rest_framework import serializers
from Apps.Life.models import Room
from Apps.Activity.models import TaskRecord


class TaskRecordSerializer(serializers.ModelSerializer):
    """查寝记录数据的序列化"""
    classname = serializers.CharField(source='student_approved.studentinfo.grade.name')
    student = serializers.CharField(source='student_approved.username')
    student_name = serializers.CharField(source='student_approved.userinfo.name')
    worker_name = serializers.CharField(source='worker.userinfo.name')

    class Meta:
        model = TaskRecord
        fields = ('id', 'classname', 'room_str', 'student', 'student_name', 'reason', 'worker_name', 'created_time')


class TaskRecordExcelSerializer(TaskRecordSerializer):
    """查寝记录数据输出excel的序列化"""
    date = serializers.SerializerMethodField()
    classname = serializers.CharField(source='student_approved.studentinfo.grade.name')

    def get_date(self, value):
        """显示日期而不是时间"""
        return value.created_time.date().strftime("%Y-%m-%d")

    class Meta:
        model = TaskRecord
        fields = ('date', 'room_str', 'classname', 'student', 'student_name', 'reason')
