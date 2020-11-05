'''
APIView:restframework框架
JsonResponse:返回json应答(默认为httpresponse)
paginator:分页器
objectdoesnotexist:查询不存在(get)抛出的异常
'''
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from . import models
# Create your views here.


class Info(APIView):
    '''
    http://127.0.0.1:8000/api/career/info
    page:10 per
    '''
    def post(self, request):
        '''
        处理post请求
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def get(self, request):
        '''
        处理get请求
        '''
        redic = request.GET
        text_id = redic.get('id',-1)
        if text_id != -1:
            ret = {
            'id':0,
            'title':"on title",
            'introduction':"on introduction",
            'body_text':"on more details",
            'creation_time':"0000.00.00"
            }
            try:
                ret_info = models.Career.objects.get(id = text_id)
            except ObjectDoesNotExist as do_not_find:
                print("no this text",do_not_find)
                error_message = {'info':"no id = "+text_id+" text!"}
                return JsonResponse(error_message)
            ret['id'] = ret_info.id
            ret['title'] = ret_info.title
            ret['introduction'] = ret_info.note
            ret['body_text'] = ret_info.note
            ret['creation_time'] = ret_info.release_time
        else:   #id不存在,查询all,并根据page返回第几页
            rets = {
                'page':-1,
                'max_page':-1,
                'list':[]
            }
            ret_page = int(redic.get('page',-1))
            if ret_page == 0:
                ret_page = 1
            if ret_page == -1:
                ret = {'message':"unexpect request!"}
                return JsonResponse(ret)
            else:
                ret = {
                    'id':"-1",
                    'title':"no title",
                    'body_text':"none",
                    'creation_time':"0000.00.00",
                    }
                rets['page'] = ret_page
                text_list = models.Career.objects.all()
                paginator = Paginator(text_list,10) #每页显示十项
                max_page = paginator.count
                rets['max_page'] = max_page
                if max_page == 0:
                    return JsonResponse({'info':"no data."})
                for i in paginator.page(ret_page):
                    ret['id'] = i.id
                    ret['title'] = i.title
                    ret['body_text'] = i.note
                    ret['creation_time'] = i.release_time
                    rets['list'].append(ret)
                return JsonResponse(rets)
        return JsonResponse({'info':"unexpect error"})

    def put(self, request):
        '''
        处理put请求
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def delete(self, request):
        '''
        处理delete请求
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)
