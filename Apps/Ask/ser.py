"""导入模型和序列化"""

from rest_framework import serializers
from . import models


class AskTypeSerializer(serializers.ModelSerializer):
    """请假类型序列化"""
    name = serializers.CharField(source="type_name")

    class Meta:
        model = models.AskType
        fields = ("id", "name")


class AskSerializer(serializers.ModelSerializer):
    """请假条序列化"""
    students_name = serializers.SerializerMethodField()
    min = serializers.SerializerMethodField()
    ask_type = serializers.SerializerMethodField()

    def get_students_name(self, obj):
        """取出关联列表的用户姓名"""
        return obj.user_id.userinfo.name

    def get_min(self, obj):
        """计算时间"""
        times = obj.end_time - obj.start_time
        hours = times.total_seconds() % (60 * 60 * 24) / 60 / 60  # 剩余的小时
        return str(times.days) + '天 ' + str(format(hours, '.1f')) + '时'

    def get_ask_type(self, obj):
        """取出请假类型"""
        return obj.ask_type.type_name

    class Meta:
        model = models.Ask
        # fields = "__all__"
        fields = (
            'id', 'students_name', 'reason', 'contact_info',
            'status', 'ask_type', 'ask_state',
            'place', 'start_time', 'end_time',
            'created_time', 'modify_time', 'min'
        )  # 包含


class AskAbbrSerializer(AskSerializer):
    """请假条简略序列化"""

    class Meta(AskSerializer.Meta):
        fields = ('id', 'reason', 'ask_type', 'place', 'start_time', 'end_time', 'students_name', 'min')


class AskAntiSerializer(serializers.Serializer):
    """请假条反序列化"""

    def create(self, validated_data):
        user = validated_data.get('user')
        validated_data_new = {
            'user_id': user,
            'status': validated_data.get('status'),
            'contact_info': validated_data.get('phone'),
            'ask_type': models.AskType.objects.get(type_name=validated_data.get('ask_type')),
            'reason': validated_data.get('reason'),
            'place': validated_data.get('place'),
            'ask_state': validated_data.get('user'),
            'start_time': validated_data.get('time_go'),
            'end_time': validated_data.get('time_back'),
            'grade_id': user.studentinfo.grade_id,
            'pass_id': user.studentinfo.grade_id.related_to_teacher.user_id
        }
        return models.Ask.objects.create(**validated_data_new)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user', instance.user_id)
        instance.status = validated_data.get('status', instance.status)
        instance.contact_info = validated_data.get('phone', instance.contact_info)
        instance.ask_type = models.AskType.objects.get(type_name=validated_data.get('ask_type', instance.ask_type))
        instance.reason = validated_data.get('reason', instance.reason)
        instance.place = validated_data.get('place', instance.place)
        instance.ask_state = validated_data.get('status', instance.ask_state)
        instance.start_time = validated_data.get('time_go', instance.start_time)
        instance.end_time = validated_data.get('time_back', instance.end_time)
        # instance.created_time
        # instance.modify_time
        instance.grade_id = instance.user_id.studentinfo.grade_id
        instance.pass_id = instance.grade_id.related_to_teacher.user_id
        instance.save()
        return instance


class AuditSerializer(serializers.ModelSerializer):
    """审批记录序列化"""
    name = serializers.CharField(source="ask_id.user_id.userinfo.name")
    place = serializers.CharField(source="ask_id.place")
    end_time = serializers.DateTimeField(source="ask_id.end_time")
    start_time = serializers.DateTimeField(source="ask_id.start_time")
    status = serializers.SerializerMethodField()
    min = serializers.SerializerMethodField()

    def get_min(self, obj):
        times = obj.ask_id.end_time - obj.ask_id.start_time
        hours = times.total_seconds() % (60 * 60 * 24) / 60 / 60  # 剩余的小时
        return str(times.days) + '天 ' + str(format(hours, '.1f')) + '时'

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = models.Audit
        # fields = "__all__"
        fields = ('name', 'status', 'place', 'created_time', 'start_time', 'end_time', 'modify_time', 'min')  # 包含
        # exclude = ('image',) # 不包含
