from rest_framework import serializers
from Apps.Attendance.models import TaskRecord


class TaskRecordSerializer(serializers.ModelSerializer):
    """查寝记录数据的序列化"""
    classname = serializers.CharField(source='student_approved.studentinfo.grade.name')
    student = serializers.CharField(source='student_approved.username')
    student_name = serializers.CharField(source='student_approved.userinfo.name')
    worker_name = serializers.CharField(source='worker.userinfo.name')

    class Meta:
        model = TaskRecord
        fields = ('id', 'classname', 'room_str', 'student', 'student_name', 'reason', 'worker_name', 'created_time')
