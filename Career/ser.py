from Manage.models import TypeChild
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
