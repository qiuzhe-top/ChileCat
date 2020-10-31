from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
# Create your views here .


class LeaveType(APIView):
    def post(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息1'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def get(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def put(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def delete(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)


class Draft(APIView):
    def post(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def get(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def put(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def delete(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)


class Audit(APIView):
    def post(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def get(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def put(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def delete(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)
