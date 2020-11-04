from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
# Create your views here.


class Info(APIView):
    '''
    http://127.0.0.1:8000/api/career/info
    page:10 per
    '''
    def post(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def get(self, request):
        '''
        处理get请求
        '''
        ret = {
            'id':0,
            'title':"on title",
            'introduction':"on introduction",
            'body_text':"on more details",
            'creation_time':"0000.00.00"
            }
        redic = request.GET
        text_id = redic.get('id',-1)
        if text_id != -1:
            #TODO(liuhai): id存在时
            pass

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
