from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.


class StudentInformation(APIView):
    def get(self, request, *args, **kwargs):
        '''
          request:
            username: 19510146 # 学号
          response:
            {
              id:1 # 学生ID
              name: 张三 # 学生姓名
              phone: 19101245412 #电话
            }
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)
