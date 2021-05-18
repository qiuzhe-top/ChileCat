from rest_framework import serializers
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
