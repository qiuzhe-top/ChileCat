from django.contrib.auth.models import User
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
        try:
            username = request.GET['username']
            user = User.objects.get(username=username)
            ret['data'] ={
                "username":username,
                "name":user.userinfo.name,
                "tel":user.userinfo.tel,
                "grade":user.studentinfo.grade.name
            }
            ret['message'] = '搜索成功'
            ret['code'] = 2000
            return JsonResponse(ret)
        except:
            ret['code'] = 4000
            ret['message'] = '没有用户或用户信息不完整'
        return JsonResponse(ret)
