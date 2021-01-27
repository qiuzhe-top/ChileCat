from .models import TypeChild
from rest_framework import serializers
from . import models

class TypeChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeChild
        # fields = "__all__"
        fields = ('id', 'title') # 包含
        #exclude = ('image',) # 不包含
class CareerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Career
        # fields = "__all__"
        fields = ('id', 'title', 'note') # 包含
        #exclude = ('image',) # 不包含
class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Career
        # fields = "__all__"
        # fields = ('id', 'title', 'note') # 包含
        exclude = ('id','source') # 不包含
class CareerForSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    note = serializers.CharField()
    text = serializers.CharField()
    source = serializers.CharField(required=False)
    viewnum = serializers.IntegerField(max_value=4)
    classify = serializers.StringRelatedField()
    class Meta:
        model = models.Career
        # fields = "__all__"
        fields = ('id', 'title', 'note','text','source','viewnum','classify') # 包含
