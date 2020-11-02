import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from . import models

# Create your views here.
class info(APIView):
    '''
    就业信息获取
    '''
    def get(self,request):
        ret = {"demo":1}
        return JsonResponse(ret)
    
    def post(self,request):
        pass
    
