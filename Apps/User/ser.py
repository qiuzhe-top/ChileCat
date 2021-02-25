from . import models
from rest_framework import serializers


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = ('id', 'name')


class TeacherForGradeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='grade.id')
    name = serializers.CharField(source='grade.name')

    class Meta:
        model = models.TeacherForGrade
        fields = ('id', 'name')


class TeacherForCollegeSerializer(serializers.ModelSerializer):
    listGrader = serializers.SerializerMethodField()

    class Meta:
        model = models.TeacherForCollege
        fields = ('listGrader',)  # 包含

    def get_listGrader(self, obj):
        d = obj.college.grade_set.all()
        ser = GradeSerializer(instance=d, many=True).data
        ret = []
        for item in ser:
            dicts = {}
            for k, v in item.items():
                dicts[k] = v
            ret.append(dicts)
        return ret
