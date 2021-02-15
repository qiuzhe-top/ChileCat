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
from Apps.User.models import UserInfo,TeacherForCollege,College,Grade,User
from Apps.User.utils.auth import get_user
from Apps.Ask.utils import ask
from . import models,ser
# from User.utils.auth import get_user
from django.db.models import Q
# Create your views here .

logger = logging.getLogger(__name__) #日志

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
        ask_type = []
        for i in Ask.models.AskType.objects.all():
            ask_type.append(i.type_name)
        ret['data'] = ask_type
        ret['code'] = 2000
        ret['message'] = "执行成功"

        return JsonResponse(ret)

class Draft(APIView):
    '''
    请假条 提交 获取
    '''
    API_PERMISSIONS = ['请假条','post','delete']

    def post(self, request):
        '''
        提交假条
        '''
        ret = {'code':2000,'message':"提示信息",}
        req = request.data
        try:
            # 获取请假条信息
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
        user_id_user = request.user
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
        relationship = {
            'default':ask.AskToStudent.view(),
            'teacher':ask.AskToTeacher.view()
            }
        ret = {'code':0000,'message':"no message",'data':{}}
        req_list = request.GET
        try:
            ask_id = int(req_list.get('id',-1))
            if ask_id != -1:
                ask = Ask.models.Ask.objects.get(id = ask_id)
                ask_list = ser.AskSerializer(instance=audit_list,many=True).data
            else:
                is_teacher = "teacher" if(
                    User.objects.filter(groups__name="teacher").exists()
                )else(
                    "default")
                ask_list = relationship.get(is_teacher)
        except ValueError as not_number:
            return JsonResponse({'code':4000,'message':"id_not_number."})
        except Ask.models.Ask.DoesNotExist:
            return JsonResponse({'code':4000,'message':"请假条:"+ask_id+"不存在"})
        ret['data'] = ask_list
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
