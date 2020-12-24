from . import models
from rest_framework import serializers

class AskSerializer(serializers.ModelSerializer):
  students_name = serializers.SerializerMethodField()
  min = serializers.SerializerMethodField()
  
  def get_students_name(self,obj):
    return obj.user_id.userinfo.name

  def get_min(self,obj):
    times = obj.end_time - obj.start_time
    hours = times.total_seconds() % (60*60*24) / 60 / 60 # 剩余的小时
    return str(times.days) + '天 ' + str(  format(hours, '.1f')   ) + '时'

  class Meta:
      model = models.Ask
      
      # fields = "__all__"
      fields = ('id', 'reason', 'ask_type','place','start_time','end_time','students_name','min') # 包含
      #exclude = ('image',) # 不包含


class AuditSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="ask_id.user_id.userinfo.name")
    place = serializers.CharField(source="ask_id.place")
    end_time = serializers.DateTimeField(source="ask_id.end_time")
    start_time = serializers.DateTimeField(source="ask_id.start_time")
    status = serializers.SerializerMethodField()
    min = serializers.SerializerMethodField()
    def get_min(self,obj):
        times = obj.ask_id.end_time - obj.ask_id.start_time
        hours = times.total_seconds() % (60*60*24) / 60 / 60 # 剩余的小时
        return str(times.days) + '天 ' + str(  format(hours, '.1f')   ) + '时'

    def get_status(self,obj):
        return obj.get_status_display()
    class Meta:
        model = models.Audit
        # fields = "__all__"
        fields = ('name', 'status','place','created_time','start_time','end_time','modify_time','min') # 包含
        #exclude = ('image',) # 不包含


