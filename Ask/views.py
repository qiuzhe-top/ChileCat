'''
必要模块引用
'''
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .models import Ask
from . import models
# Create your views here .


class LeaveType(APIView):
    '''
    请假功能
    '''
    def post(self, request):
        '''
        default post request
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息1'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def get(self, request):
        '''
        获取请假类别
        /api/ask/leave_type
        '''
        ret = {'code':0000,'message':"提示信息",'data':[]}
        ask_data = {'id':0,'name':"null"}
        data_list = models.Ask.objects.all()
        for i in data_list:
            ask_data['id'] = i.id
            ask_data['name'] = i.ask_type
            ret['data'].append(ask_data)
        ret['code'] = 2000
        ret['message'] = "执行成功"
        return JsonResponse(ret)

    def put(self, request):
        '''
        default put request
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def delete(self, request):
        '''
        default delete request
        '''
        ret = {'code':0000,'message':"提示信息"}
        return JsonResponse(ret)


class Draft(APIView):
    '''
    学生创建请假条/创建草稿
    '''
    def post(self, request):
        '''
        提交假条
        '''
        ret = {'code':2000,'message':"提示信息",}
        req = request.POST
        try:
            leave_type = req['leave_type']
            time_go = req['time_go']
            time_back = req['time_back']
            place = req['place']
            reason = req['reason']
            phone = req['phtone']
            state = req['state']
        except KeyError as req_failed:
            print("get key failed",req_failed)
            ret['code'] = 4000
            ret['message'] = "执行失败"
            return JsonResponse(ret)
        unit = Ask(
            #TODO(liuhai) id锁定为1
            user_id = 1,
            status = state,
            contact_info = phone,
            reason = reason,
            place = place,
            ask_type = leave_type,
            start_time = time_go,
            end_time = time_back,
            )
        unit.save()
        ret['code'] = 2000
        ret['message'] = "创建成功 / 草稿保存成功"
        return JsonResponse(ret)

    def get(self, request):
        '''
        获取多个请假条简单信息,分页,获取详细信息
        /api/ask/draft
        备注
        ID与page同时存在时id优先展示
        grade_id:只有教师权限请求才有用 存在时为后台老师获取班级所有的请假条并且进行分页
        '''
        ret = {'code':0000,'message':"no message",'data':{}}
        req_list = request.GET
        ask_id = req_list.get('id',-1)

        if ask_id != -1:
            try:
                ask = models.Ask.objects.get(id = ask_id)
            except ObjectDoesNotExist as get_failed:
                print("get failed",get_failed)
                ret['code'] = 4000
                ret['message'] = "没有此id的请假条"
                return JsonResponse(ret)
            ret['data'] = {
                'user_id': ask.user_id,
                'status': ask.status,
                'constact_info': ask.constact_info,
                'ask_type': ask.ask_type,
                'reason': ask.reason,
                'place': ask.place,
                'ask_state': ask.ask_state,
                'start_time': ask.start_time,
                'end_time': ask.end_time,
                'created_time': ask.created_time,
                'modify_time': ask.modify_time,
            }
            return JsonResponse(ret)
        else:
            req_page = int(req_list.get('page',-1))
            if req_page == 0:
                req_page =1
            print(req_page)
            if req_page == -1:
                ret['code'] = 4000
                ret['message'] = "错误的请求方式,至少有'page','id'其中之一"
                return JsonResponse(ret)
            ret['data'] = {'list':[]}
            ask_unit = {
                'text': "请假类型+15字简介",
		        'start_time': "开始时间",
		        'vacate_time': "请假时长",
		        'state': "状态",
		        'state_level': "目前审核状态"
            }
            ask_all_list = models.Ask.objects.all()
            paginator = Paginator(ask_all_list,10)
            max_page = paginator.num_pages
            print(paginator.num_pages)
            if max_page < 1:
                ret['code'] = 4000
                ret['message'] = "没有任何数据"
                return JsonResponse(ret)
            if req_page > max_page:
                req_page = max_page
            for i in paginator.page(req_page):
                ask_unit['text'] = i.ask_type
                ask_unit['start_time'] = i.start_time
                ask_unit['vacate_time'] = i.end_time - i.start_time
                ask_unit['state'] = i.status
                ask_unit['state_level'] = i.ask_state
                ret['page']['list'].append(ask_unit)
            ret['page'] = req_page
        return JsonResponse(ret)
        #TODO(liuhai) 写到 获取多个请假条简单信息 分页 获取详细信息,剩下自己加油

    def put(self, request):
        '''
        学生修改请假条信息
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def delete(self, request):
        '''
        default delete request
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)


class Audit(APIView):
    '''
    老师审核请假条
    '''
    def post(self, request):
        '''
        default post request
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def get(self, request):
        '''
        default get request
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def put(self, request):
        '''
        审核通过 审核不通过 撤销已通过的审核
        1=通过 2=不通过
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def delete(self, request):
        '''
        default delete request
        '''
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)
