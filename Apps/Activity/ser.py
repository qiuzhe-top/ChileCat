from rest_framework import serializers
from .models import *


class ManageSerializer(serializers.ModelSerializer):
    """查寝记录数据的序列化"""
    college = serializers.SerializerMethodField()

    def get_college(self, value: Manage):
        return value.college.name

    class Meta:
        model = Manage
        fields = ('id', 'college', 'console_code', 'code_name')
