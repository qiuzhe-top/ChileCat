from . import models
from rest_framework import serializers
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = ('id','name')

class TeacherForGradeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='grade_id.id')
    name = serializers.CharField(source='grade_id.name')
    class Meta:
        model = models.TeacherForGrade
        fields = ('id','name')

class TeacherForCollegeSerializer(serializers.ModelSerializer):
    listGrader = serializers.SerializerMethodField()

    class Meta:
        model = models.TeacherForCollege
        fields = ('listGrader',) # 包含
    def get_listGrader(self,obj):
        ret = []
        d = obj.college_id.grade_set.all()
        ser = GradeSerializer(instance=d,many=True).data
        print(ser)
        return ser