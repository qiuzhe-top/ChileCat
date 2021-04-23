from rest_framework.views import APIView
from django.http import JsonResponse
from Apps.Activity.utils.activity_factory import ActivityFactory
from .utils.exceptions import *
from .models import *
from .ser import ManageSerializer
from .utils.permission import AttendancePermission
from Apps.Activity.utils.activity_operate import AttendanceActivityControl
import json

# Create your views here.


class SwitchKnowing(APIView):
    """控制活动"""
    API_PERMISSIONS = ['活动开关', 'get','post','put']
    permission_classes = []

    def get(self, request):
        """获取当前是否开启活动"""
        ret = {
            'code': 0000,
            'message': "default message",
            'data': ""
        }
        flag = ActivityFactory(self.request.query_params['act_id']).get_status()
        ret['code'] = 2000
        ret['message'] = "状态获取成功"
        ret['data'] = flag
        return JsonResponse(ret)

    def post(self, request):
        """切换活动状态(开/关)"""
        ret = {}
        ret['data'] = ActivityFactory(self.request.data['id']).switch()
        ret['code'] = 2000
        ret['message'] = "状态重置成功"
        return JsonResponse(ret)

    def put(self, request):
        """初始化活动,怎么初始化由底层决定"""
        ret = {
            'code': 0000,
            'message': "default message"
        }
        try:
            ActivityFactory(self.request.query_params['act_id']).initialization()
            ret['code'] = 2000
            ret['message'] = "状态重置成功"
        except DormitoryEveningCheckException as e:
            ret['code'] = 4000
            ret['message'] = str(e)
        return JsonResponse(ret)


class VerificationCode(APIView):
    """活动验证码"""

    API_PERMISSIONS = ['工作验证码', 'get', '*post','*put']
    permission_classes = [AttendancePermission,]

    def get(self, request):
        """获取验证码"""
        act_id = request.data['id']
        ret = {
            'code': 2000,
            'message': "获取成功",
            'data': AttendanceActivityControl(act_id).get_verification_code()
        }
        return JsonResponse(ret)

    def put(self, request):
        """生成验证码"""
        ret = {
            'code': 2000, 'message': "生成验证码成功",
            'data': ActivityFactory(self.request.query_params['act_id']).generate_verification_code()
        }
        return JsonResponse(ret)

    def post(self, request):
        """验证验证码"""
        ret = {
            'code': 0000,
            'message': "default message"
        }
        req_list = self.request.data
        req_id_code = req_list.get('idcode', -1)
        if ActivityFactory(self.request.query_params['act_id']).verify(req_id_code):
            ret['code'] = 2000
            ret['message'] = "验证成功"
        else:
            ret['code'] = 4000
            ret['message'] = "验证失败"
        return JsonResponse(ret)

class MyActive(APIView):
    """我的活动"""
    API_PERMISSIONS = ['我的活动', '*get']
    def get(self, request):
        """能开什么活动"""
        ret = {'code': 4000, 'message': "default", 'data': ''}
        role = request.GET['role']
        pers = request.user.get_all_permissions()
        perms = []
        if role == "activity_admin":
            for per in pers:
                if per.find('manage') > 0:
                    perms.append(per[per.find('-')+1:])
            act_list = Manage.objects.filter(code_name__in=perms)
            ret['data'] = ManageSerializer(instance=act_list, many=True).data
            ret['code'] = 2000
            ret['message'] = "管理员获取"
        elif role == "attendance_worker":
            for per in pers:
                if per.find('evening_study') > 0:
                    p = per[per.find('.')+1:]
                    m = Manage.objects.get(code_name=p)
                    perms.append({
                        "title":m.college.name + "-晚自修检查",
                        "type":m.types
                    })
                elif per.find('floor-dorm') > 0:
                    perms.append({
                        "title":per[per.find('_')+1:]+"号楼查寝",
                        "type":"floor-dorm"

                    })
                elif per.find('floor-health') > 0:
                    perms.append({
                        "title":per[per.find('_')+1:]+"号楼卫生检查",
                        "type":"floor-health"

                    })
            print(perms)
            ret['data'] = perms
            ret['code'] = 2000
            ret['message'] = "工作人员获取"
        return JsonResponse(ret)

class SaveRoster(APIView):
    '''保存班表'''
    def post(self, request, *args, **kwargs):
        ret = {}
        try:
            roster = request.data['roster']
            manage_id = request.data['id']
        except:
            ret['message'] = '参数异常'
            ret['code'] = 4000
        try:
            ActivityFactory(manage_id).save_roster(roster)
        except:
            ret['message'] = '保存失败'
            ret['code'] = 4000
        ret['message'] = '保存成功'
        ret['code'] = 2000
        return JsonResponse(ret)
