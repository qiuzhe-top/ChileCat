from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
class LeaveType(APIView):
    def post(self, request): 
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息1'
        ret['data'] = 'data'
    def get(self,request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
    def put(self,request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
    def delete(self,request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'


class Draft(APIView):
    def post(self, request): 
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
    def get(self,request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
    def put(self,request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
    def delete(self,request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'


# class Drafts(APIView):
#     def post(self, request): 
#         ret = {}
#         ret['code'] = '2000'
#         ret['message'] = '提示信息'
#         ret['data'] = 'data'
#     def get(self,request):
#         ret = {}
#         ret['code'] = '2000'
#         ret['message'] = '提示信息'
#         ret['data'] = 'data'
#     def put(self,request):
#         ret = {}
#         ret['code'] = '2000'
#         ret['message'] = '提示信息'
#         ret['data'] = 'data'
#     def delete(self,request):
#         ret = {}
#         ret['code'] = '2000'
#         ret['message'] = '提示信息'
#         ret['data'] = 'data'

class Audit(APIView):
    def post(self, request): 
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
    def get(self,request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
    def put(self,request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
    def delete(self,request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
