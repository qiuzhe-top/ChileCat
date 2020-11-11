'''
必要模块引用
'''
import json
import pytz
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Ask
from User.models import User
from . import models
from User.utils.auth import get_user
# Create your views here .


class LeaveType(APIView):
    '''
    请假功能
    '''
    def get(self, request):
        '''
        获取请假类别
        /api/ask/leave_type
        '''
        ret = {'code':0000,'message':"提示信息",'data':[]}
        # ask_data = {'id':0,'name':"null"}
        # data_list = models.Ask.objects.all()
        # for i in data_list:
        #     ask_data['id'] = i.id
        #     ask_data['name'] = i.ask_type
        #     ret['data'].append(ask_data)
        ask_type = [
            # {'id':"0",'title':"外出"},
            # {'id':"1",'title':"事假"},
            # {'id':"2",'title':"其他"}
            '外出',
            '事假',
            '其他'
        ]
        print(get_user(request))
        ret['data'] = ask_type
        ret['code'] = 2000
        ret['message'] = "执行成功"

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
            phone = req['phone']
            state = req['state']
            
        except KeyError as req_failed:
            print("get key failed",req_failed)
            ret['code'] = 4000
            ret['message'] = "执行失败,key_get_exception."
            return JsonResponse(ret)
            #TODO(liuhai) id锁定为1
        
        user_id_user = get_user(request)# User.objects.get(id = 1)
        unit = Ask(
            user_id = user_id_user,
            status = state,
            contact_info = phone,
            reason = reason,
            place = place,
            ask_type = leave_type,
            start_time = time_go,
            end_time = time_back,
            )
        print(unit)
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
        ask_id = int(req_list.get('id',-1))
        if ask_id != -1:
            try:
                ask = models.Ask.objects.get(id = ask_id)
                print(ask.created_time)
            except ObjectDoesNotExist as get_failed:
                print("get failed",get_failed)
                ret['code'] = 4000
                ret['message'] = "没有此id的请假条"
                return JsonResponse(ret)
            ret['data'] = {
                'user_id': ask.user_id.id,
                'status': ask.status,
                'constact_info': ask.contact_info,
                'ask_type': ask.ask_type,
                'reason': ask.reason,
                'place': ask.place,
                'ask_state': ask.ask_state,
                'start_time': ask.start_time,
                'end_time': ask.end_time,
                'created_time': ask.created_time,
                'modify_time': ask.modify_time,
            }
            ret['code'] = 2000
            ret['message'] = "success"
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
            if req_page > max_page:
                print("页数有误(超出最大页数)")
                ret['code'] = 4000
                ret['message'] = "page_out_of_max"
                return JsonResponse(ret)
            print(paginator.num_pages)
            if max_page < 1:
                ret['code'] = 4000
                ret['message'] = "没有任何数据"
                return JsonResponse(ret)
            if req_page > max_page:
                req_page = max_page
            for i in paginator.page(req_page):
                ask_unit['text'] = i.ask_type
                ask_unit['reason'] = i.reason
                ask_unit['start_time'] = i.start_time
                ask_unit['vacate_time'] = i.end_time - i.start_time
                ask_unit['state'] = i.status
                ask_unit['state_level'] = i.ask_state
                ret['data']['list'].append(ask_unit)
            ret['page'] = req_page
            ret['code'] = 2000
        return JsonResponse(ret)

    def put(self, request):
        '''
        学生修改请假条信息
        '''
        ret = {
            'code':0000,
            'message':"default message"
            }
        req = request.data
        print(req)
        try:
            #读取前端假条修改数据
            ask_id = req['id']
            leave_type = req['leave_type']
            time_go = req['time_go']
            time_back = req['time_back']
            place = req['place']
            reason = req['reason']
            phone = req['phone']
            state = req['state']
        except KeyError as lack_info:
            print("缺少条目",lack_info)
            ret['code'] = 4000
            ret['message'] = "lack_list_expectation."
            return JsonResponse(ret)
        #TODO(liuhai) 时间解析未完成
        # try:
        #     time_go = timezone.datetime.strptime(time_go,"%Y-%m-%d ")
        #     time_back = timezone.datetime.strptime(time_back,"%Y-%m-%d")
        # except ValueError as time_form_error:
        #     print("时间格式有误",time_form_error)
        #     ret['code'] = 4000
        #     ret['message'] = "time_form_exception"
        #     return JsonResponse(ret)
        print(time_back)
        print(time_go)
        if leave_type == "1":
            leave_type = "out"
        elif leave_type == "2":
            leave_type = "leave"
        else:
            leave_type = "other"
        try:
            ask_unit = models.Ask.objects.get(id = ask_id)
        except ObjectDoesNotExist as not_find_ask:
            print("请假条不存在",not_find_ask)
            ret['code'] = 4000
            ret['message'] = "ask_not_find"
        #存入数据
        ask_unit.ask_type = leave_type
        ask_unit.start_time = time_go
        ask_unit.end_time = time_back
        ask_unit.place = place
        ask_unit.reason = reason
        ask_unit.contact_info = phone
        ask_unit.status = state
        ask_unit.save()
        ret['code'] = 2000
        ret['message'] = "修改成功"
        return JsonResponse(ret)

class Audit(APIView):
    '''
    老师审核请假条
    '''
    def put(self, request):
        '''
        审核通过 审核不通过 撤销已通过的审核
        1=通过 2=不通过
        '''
        ret = {
            'code':0000,
            'message':"default info."
        }
        req_list = request.data
        ask_id = req_list.get('id',-1)
        operate_sate = req_list.get('operate_sate',-1)
        if ask_id == -1 or operate_sate == -1:
            print("条件缺损")
            ret['code'] = 4000
            ret['message'] = "修改失败(条件缺损)"
            return JsonResponse(ret)
        try:
            ask_unit = models.Ask.objects.get(id = ask_id)
        except ObjectDoesNotExist as not_find:
            print("没有找到记录",not_find)
            ret['code'] = 4000
            ret['message'] = "修改失败(没有找到请假条)"
            return JsonResponse(ret)
        ask_unit.status = operate_sate
        ask_unit.save()
        ret['code'] = 2000
        ret['message'] = "修改成功"
        return JsonResponse(ret)
