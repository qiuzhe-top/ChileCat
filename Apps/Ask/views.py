'''
必要模块引用
'''
import json
import logging
from datetime import datetime
import pytz
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from Apps import Ask
from Apps.User.models import User,UserInfo,TeacherForCollege,College,Grade
from Apps.User.utils.auth import get_user
from . import models,ser
# from User.utils.auth import get_user
from django.db.models import Q
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields import DateTimeField
# Create your views here .

logger = logging.getLogger(__name__) #日志


def to_dict(obj, fields=None, exclude=None):
    '''
    自定义to_dict
    '''
    data = {}
    for fun in obj._meta.concrete_fields + obj._meta.many_to_many:
        value = fun.value_from_object(obj)
        if fields and fun.name not in fields:
            continue
        if exclude and fun.name in exclude:
            continue
        if isinstance(fun, ManyToManyField):
            value = [i.id for i in value] if obj.pk else None
        if isinstance(fun, DateTimeField):
            value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
        data[fun.name] = value
    return data

class LeaveType(APIView):
    '''
    请假类别
    '''
    def get(self, request):
        '''
        获取请假类别
        /api/ask/leave_type
        '''
        ret = {'code':0000,'message':"提示信息",'data':[]}
        ask_type = [
            # {'id':"0",'title':"外出"},
            # {'id':"1",'title':"事假"},
            # {'id':"2",'title':"其他"}
            '外出',
            '事假',
            '病假',
            '其他'
        ]
        # print(public_permissions)
        ret['data'] = ask_type
        ret['code'] = 2000
        ret['message'] = "执行成功"

        return JsonResponse(ret)

class Draft(APIView):
    '''
    请假条 提交 获取
    '''
    def post(self, request):
        '''
        提交假条
        '''
        ret = {'code':2000,'message':"提示信息",}
        req = request.data
        try:
            leave_type = req['leave_type']
            time_go = req['time_go']
            time_back = req['time_back']
            place = req['place']
            reason = req['reason']
            phone = req['phone']
            status = req['status']
        except KeyError as req_failed:
            print("get key failed",req_failed)
            ret['code'] = 4000
            ret['message'] = "执行失败,key_get_exception."
            return JsonResponse(ret)
        user_id_user = get_user(request)# 获取用户
        try:
            grade_id = user_id_user.studentinfo.grade_id
            #(liuhai) 这里的捕获可能不对
        except User.DoesNotExist:
            ret['code'] = 5000
            ret['message'] = "用户信息不完整无法请假"
            return JsonResponse(ret)

        #默认只给第一个管理老师审核
        try:
            pass_id = grade_id.teacherforgrade_set.all().first().user_id
        except AttributeError as no_teacher_gov:
            print("该用户没有对应的审批老师关系 ", no_teacher_gov)
            return JsonResponse({'code':4000,'message':"没有审批老师"})
        unit = models.Ask(
            user_id = user_id_user,
            status = status,
            contact_info = phone,
            reason = reason,
            place = place,
            ask_type = leave_type,
            start_time = time_go,
            end_time = time_back,
            grade_id = grade_id,
            pass_id = pass_id
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
        try:
            ask_id = int(req_list.get('id',-1))
            ask_type = req_list.get('type',-1)
            class_id = req_list.get('classid',-1)
        except ValueError as not_number:
            # print("id不是数字",not_number)
            return JsonResponse({'code':4000,'message':"id_not_number."})
        has_type = 0 if ask_type == -1 else 1   #是否存在type
        if ask_id != -1:                                    #是否存在id字段,如果有,则是单记录读取
            try:
                ask = Ask.models.Ask.objects.get(id = ask_id)
                # print(ask.created_time)
            except ObjectDoesNotExist as get_failed:
                # print("get failed",get_failed)
                ret['code'] = 4000
                ret['message'] = "没有此id的请假条"
                return JsonResponse(ret)
            # print(ask.ask_type)
            # ret['data'] = {
            #     'user_id': ask.user_id.id,
            #     'status': ask.status,
            #     'constact_info': ask.contact_info,
            #     'ask_type': ask.ask_type,
            #     'reason': ask.reason,
            #     'place': ask.place,
            #     'ask_state': ask.ask_state,
            #     'start_time': ask.start_time.strftime('%Y-%m-%d %H:%M'),
            #     'end_time': ask.end_time.strftime('%Y-%m-%d %H:%M')
            # }
            ask_dict = ask.__dict__
            ask_dict.pop('_state')
            ret['data'] = ask_dict
            # print(ret['data'])
            ret['code'] = 2000
            ret['message'] = "success"
            return JsonResponse(ret)
            # id字段的查询完毕
        else:                                   #如果没有id字段,则根据条件返回不同的list
            user_unit_id = get_user(request) #返回结果为用户的id字段
            if user_unit_id == -1:
                return JsonResponse({'code':4000,'message':"用户不存在"})
            try:
                user_auth = UserInfo.objects.get(user_id = user_unit_id)    #获取用户权限
                # print("用户: ",user_auth)
            except ObjectDoesNotExist as user_not_find:
                print("user not exist. ",user_not_find)
                return JsonResponse({'code':4000,'message':"此用户没有在用户权限表中存在"})
            if user_auth.identity == "teacher": #用户是老师
                #(zouyang): classid:1
                class_id = req_list.get('classid',-1)
                # if history != -1 or class_id != -1:
                if class_id != -1:
                    ret_list = []
                    class_id = Grade.objects.get(id = class_id)
                    ret_list = Ask.models.Ask.objects.filter(grade_id=class_id,status=1)
                    data = ser.AskSerializer(instance=ret_list,many=True).data
                    ret['data']['list'] = data
                else:
                    return JsonResponse({'code':4000,'message':"没有管理的班级或其他意外的错误"})
                    print("in else!")
                ret['code'] = 2000
                ret['message'] = "查询成功,查询用户为老师"
                return JsonResponse(ret)
            elif user_auth.identity == "college":     #需要领导审核的
                ask_list = Ask.models.Ask.objects.filter(
                    Q(status = 2) & Q(grade_id = class_id)
                    )
                print(ask_list)
                data = ser.AskSerializer(instance=ask_list,many=True).data
                ret['data'] = {'list':data}
                ret['code'] = 2000
                ret['message'] = "查询成功,查询用户为领导"
                print("查询成功,查询用户为领导")
                return JsonResponse(ret)
            elif user_auth.identity == "student":
                ask_list = Ask.models.Ask.objects.filter(
                    user_id = user_unit_id,status__in = ask_type
                    ) #[1,2]
                print(ask_type)
                ret['data'] = {'list':[]}
                for i in ask_list:
                    ask_unit = {
                        'ask_id':i.id,          #请假表id
                        'ask_status':i.status,  #审核状态
                        'ask_type':i.ask_type,  #请假类型
                        'ask_reason':i.reason,  #请假理由
                        'ask_place':i.place,    #去往地点
                        'ask_start_time':i.start_time,    #开始时间
                        'ask_end_time':i.end_time,    #结束时间
                    }
                    ret['data']['list'].append(ask_unit)
                ret['code'] = 2000
                ret['message'] = "查询成功,查询用户为学生"
                return JsonResponse(ret)
            else:
                return JsonResponse({'message':"other out"})
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
        # print(req)
        try:
            #读取前端假条修改数据
            ask_id = req['id']
            leave_type = req['leave_type']
            time_go = req['time_go']
            time_back = req['time_back']
            place = req['place']
            reason = req['reason']
            phone = req['phone']
            status = req['status']
        except KeyError as lack_info:
            print("缺少条目",lack_info)
            ret['code'] = 4000
            ret['message'] = "lack_list_expectation."
            return JsonResponse(ret)
        try:
            ask_unit = Ask.models.Ask.objects.get(id = ask_id)
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
        ask_unit.status = status
        # print(status,phone)
        ask_unit.save()
        ret['code'] = 2000
        ret['message'] = "修改成功"
        return JsonResponse(ret)

    def delete(self,request):
        '''
        学生撤销请假条
        '''
        ret = {'code':0000,'message':'default message'}
        req_list = request.data
        '''
        回传数据:id = 2
        '''
        try:
            ask_id = int(req_list.get('id',-1))
            ask_unit = Ask.models.Ask.objects.get(id = ask_id)
            ask_unit.delete()
            ret['code'] = 2000
            ret['message'] = "删除成功"
        except ObjectDoesNotExist as e:
            ret['code'] = 4000
            ret['message'] = "此请假条不存在,可能已被删除"
        finally:
            return JsonResponse(ret)

class Audit(APIView):
    '''
    老师审核请假条
    '''
    def put(self, request):
        '''
        逻辑可以改为:
                获取前端的各种数据,包括且不仅限于:
                    1,用户的身份,正常情况下只能是老师和领导两个身份才有资格访问
                    2,请假条的id,用于获取要审批的请假条
                    3,修改后的状态,用于处理请假条的去留问题
                if 身份 = 老师:
                    if请假条的old_status确实是1:
                        老师提交上级或者是直接通过
                    else(也就是目前请假条的old_status不是1了,被学生撤销了或者被其他老师审核了):
                        请刷新页面
                else if 身份 = 领导:
                    if请假条old_status = 2(等待二级领导审核):
                        领导选择通过或者是不通过
                    else(被其他领导审核了):
                        请刷新页面
                else(既不是老师也不是领导):
                    你是来捣乱的吧/或者就是特殊的管理员权限(后门权限)
                再进行添加审核表的操作

        '''
        ret = {
            'code':0000,
            'message':"default info."
        }
        user_id = get_user(request)
        try:
            #用户身份
            user_type = UserInfo.objects.get(user_id = user_id).identity
        except ObjectDoesNotExist as e:
            # print("此用户没有用户信息",e)
            ret = {
            'code':4000,
            'message':"用户没有用户信息,请联系管理员."
            }
            return JsonResponse(ret)
        req_list = request.data
        ask_id = req_list.get('id',-1)
        #前端提交修改后请假条应该处于的状态:2,领导审核 3,直接完成 4,不通过
        operate_sate = req_list.get('operate_sate',-1)
        #审核说明
        statement = req_list.get('statement',"")
        if ask_id == -1 or operate_sate == -1:
            # print("条件缺损")
            ret['code'] = 4000
            ret['message'] = "修改失败(条件缺损)"
            return JsonResponse(ret)

        try:
            ask_unit = Ask.models.Ask.objects.get(id = ask_id)
        except ObjectDoesNotExist as not_find:
            # print("没有找到记录",not_find)
            ret['code'] = 4000
            ret['message'] = "修改失败(没有找到请假条)"
            return JsonResponse(ret)
        #交给上级
        '''
            如果是要提交上级领导,并且操作的用户是老师
                1,理论上
        '''
        if operate_sate == 2 and user_type == "teacher":
            college_teacher_id = ask_unit.grade_id.college_id.teacherforcollege_set.first().user_id
            ask_unit.pass_id = college_teacher_id
            #默认第一个领导(假设只有一个)
            ask_unit.save()

        old_status = Ask.models.Ask.objects.get(id = ask_id).status
        if old_status=="1" and user_type == "teacher":
            ask_unit.status = operate_sate
            ask_unit.save()
            ret['message'] = "修改成功"
            #审核完成后把记录放入审核情况表
            unit = Ask.models.Audit(
                user_id=user_id,ask_id=ask_unit,status=operate_sate,explain=statement
                )
            unit.save()
            ret['message'] = "修改成功,记录已储存"
            ret['code'] = 2000
        elif old_status=="2" and user_type == "college":
            ask_unit.status = operate_sate
            ask_unit.save()
            ret['message'] = "修改成功"
            ret['code'] = 2000
        else:
            ret['message'] = "用户已被审核，请刷新页面"
            ret['code'] = 4006
        return JsonResponse(ret)
    def get(self,request):
        '''
        查看历史记录
        /Audit
        '''
        ret = {'code':0000,'message':"default message."}
        #(liuhai) 查找此用户的所有审批记录
        user_id = get_user(request)
        req = request.GET
        print(req)
        class_id = int(req.get('classid',-1))
        print(class_id)
        try:
            class_id = Grade.objects.get(id = class_id)
            print(class_id)
            audit_list = models.Audit.objects.filter(
                Q(user_id = user_id) & Q(ask_id__grade_id__name = class_id)
                )
            print(audit_list)
            #audit_ret_list = ser.AuditSerializer(instance=audit_list,many=True).data
            audit_ret_list = ser.AuditSerializer(instance=audit_list,many=True).data
            print(audit_ret_list)
            ret['data'] = {'list':audit_ret_list}
            ret['code'] = 2000
            ret['message'] = "查询成功"
        except ObjectDoesNotExist as e:
            print("查找错误",e)
            ret['message'] = e
        except TypeError as e:
            print("类型错误 ",e)
        finally:
            return JsonResponse(ret)

# 班级+学号 获取姓名
class GetName(APIView):
    def get(self, request, *args, **kwargs):
        ret = {}
        class_name = request.data['classname']
        sno = request.data['sno']
        user.objects.get()
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)
