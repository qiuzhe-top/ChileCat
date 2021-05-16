from rest_framework import serializers
from . import models


class Task(serializers.ModelSerializer):
    """审批记录序列化"""

    name = serializers.SerializerMethodField()
    id = serializers.IntegerField(source="task.id")
    is_open = serializers.IntegerField(source="task.is_open")
    is_builder = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.task.college.name + " " + obj.task.get_types_display()

    def get_is_builder(self, obj):
        return obj.task.user == obj.user

    class Meta:
        model = models.TaskPlayer
        fields = ('id', 'is_admin', 'is_open', 'name', 'is_builder')  # 包含
