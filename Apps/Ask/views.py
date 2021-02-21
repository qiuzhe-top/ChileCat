"""
必要模块引用
"""
import logging
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from Apps import Ask
from Apps.User.models import Grade, User
from django.contrib.auth.models import AnonymousUser
from Apps.Ask.utils import ask, audit, exceptions
from . import models, ser
from django.db.models import Q

# Create your views here .

logger = logging.getLogger(__name__)  # 日志


class LeaveType(APIView):
    """
    请假类别
    """

    @staticmethod
    def get(request):
        """
        获取请假类别
        /api/ask/leave_type
        """
        ret = {'code': 0000, 'message': "提示信息", 'data': []}
        # ask_type = ser.AskTypeSerializer(instance=Ask.models.AskType.objects.all(), many=True).data
        ask_type = []
        for i in Ask.models.AskType.objects.all():
            ask_type.append(i.type_name)
        ret['data'] = ask_type
        ret['code'] = 2000
        ret['message'] = "执行成功"

        return JsonResponse(ret)


class Draft(APIView):
    """
    请假条 提交 获取
    """
    API_PERMISSIONS = ['请假条', 'post', 'delete']

    def post(self, request):
        """
        提交假条
        """
        ret = {'code': 2000, 'message': "提示信息", }
        req = self.request.data
        req['user'] = self.request.user
        se = ser.AskAntiSerializer(instance=Ask)
        se.create(req)
        ret['code'] = 2000
        ret['message'] = "提交成功"
        return JsonResponse(ret)

    def get(self, request):
        """
        获取多个请假条简单信息,分页,获取详细信息
        /api/ask/draft
        备注
        ID存在则使用单个匹配模式
        否则按照身份获取
        """
        ret = {'code': 0000, 'message': "no message", 'data': {}}
        req_list = self.request.query_params
        # self.request.user = User.objects.get(username="19530226")
        if self.request.user == AnonymousUser:
            ret['message'] = "没有用户"
            ret['code'] = 2000
            return JsonResponse(ret)
        try:
            ask_id = int(req_list.get('id', -1))
            view_type = req_list.get('type', None)
            monitor = req_list.get('monitor', None)
            ask_list = Ask.utils.ask.AskOperate(self.request.user).view(ask_id, view_type, monitor)
            ret['data'] = ask_list
            ret['message'] = "获取成功"
            ret['code'] = 2000
        except TypeError:
            return JsonResponse({'code': 4000, 'message': "缺少id"})
        except Ask.models.Ask.DoesNotExist:
            ret['message'] = "没有此id的请假条"
            ret['code'] = 4000
        return JsonResponse(ret)

    def put(self, request):
        """
        学生修改请假条信息
        """
        ret = {
            'code': 0000,
            'message': "default message"
        }
        req = self.request.data
        ask_id = req.get('id')
        try:
            if Ask.utils.ask.AskToStudent(self.request.user).modify(ask_id, req):
                ret['message'] = "修改成功"
                ret['code'] = 2000
            else:
                ret['message'] = "修改失败"
                ret['code'] = 4000
        except exceptions.AskException as ask_except:
            ret['message'] = str(ask_except)
            ret['code'] = 4000
        return JsonResponse(ret)

    def delete(self, request):
        """
        学生撤销请假条
        """
        ret = {'code': 0000, 'message': 'default message'}
        req_list = self.request.data
        if Ask.utils.ask.AskToStudent.delete(req_list.get('id')):
            ret['code'] = 2000
            ret['message'] = "撤销成功"
        else:
            ret['code'] = 4000
            ret['message'] = "操作失败"
        return JsonResponse(ret)


class Audit(APIView):
    """
    老师审核请假条
    """

    def put(self, request):
        """
        老师控制请假条status
        逻辑:先给班主任,然后给辅导员，然后辅导员选择是否给上级领导
        """
        ret = {
            'code': 0000,
            'message': "default info."
        }
        self.request.user = User.objects.get(username="19530226")
        ask_id = self.request.data.get('id', None)
        operate_sate = self.request.data.get('operate_sate')
        try:
            audit.AuditOperate(self.request, ask_id).audit(operate_sate)
            ret['message'] = "操作成功"
            ret['code'] = 2000
        except exceptions.AuditException as audit_error:
            ret['message'] = str(audit_error)
            ret['code'] = 4000
        return JsonResponse(ret)

    def get(self, request):
        """
        查看历史记录
        /Audit
        """
        ret = {'code': 0000, 'message': "default message."}
        #  查找此用户的所有审批记录
        user_id = self.request.user
        req = self.request.query_params
        # TODO 占坑 同样的不急
        print(req)
        class_id = int(req.get('classid', -1))
        print(class_id)
        try:
            class_id = Grade.objects.get(id=class_id)
            print(class_id)
            audit_list = models.Audit.objects.filter(
                Q(user_id=user_id) & Q(ask_id__grade_id__name=class_id)
            )
            print(audit_list)
            # audit_ret_list = ser.AuditSerializer(instance=audit_list,many=True).data
            audit_ret_list = ser.AuditSerializer(instance=audit_list, many=True).data
            print(audit_ret_list)
            ret['data'] = {'list': audit_ret_list}
            ret['code'] = 2000
            ret['message'] = "查询成功"
        except ObjectDoesNotExist as e:
            print("查找错误", e)
            ret['message'] = e
        except TypeError as e:
            print("类型错误 ", e)
        finally:
            return JsonResponse(ret)


# 班级+学号 获取姓名
class GetName(APIView):
    def get(self, request):
        # TODO 班级+学号获取姓名(为什么不放在user?)
        ret = {}
        class_name = self.request.data['classname']
        sno = self.request.data['sno']
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)
