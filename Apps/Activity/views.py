from rest_framework.views import APIView
from django.http import JsonResponse
from Apps.Activity.utils.activity_factory import ActivityFactory
from .utils.exceptions import *
from .models import *
from .ser import ManageSerializer


# Create your views here.


class SwitchKnowing(APIView):
    """控制活动"""
    API_PERMISSIONS = ['活动开关', 'get']

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
        ret = {
            'code': 2000, 'message': "切换成功",
            'data': ActivityFactory(self.request.query_params['act_id']).switch()
        }
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
    """获取能开什么活动"""

    API_PERMISSIONS = ['工作验证码', 'get', 'post']

    def get(self, request):
        """能开什么活动"""
        ret = {'code': 4000, 'message': "default", 'data': ''}
        role = self.request.query_params['role']
        pers = self.request.user.get_all_permissions()
        perms = []
        if role == "activity_admin":
            for per in pers:
                if "Activity.attendance-" in per and per[-5:] == "admin":
                    perms.append(str(per).split('.')[1])
            act_list = Manage.objects.filter(code_name__in=perms)
            ret['data'] = ManageSerializer(instance=act_list, many=True).data
            ret['code'] = 2000
            ret['message'] = "管理员获取"
        elif role == "attendance_worker":
            for per in pers:
                if "Activity.attendance-" in per and per[-5:] != "admin":
                    perms.append(str(per).split('.')[1])
            act_list = Manage.objects.filter(code_name__in=perms)
            ret['data'] = ManageSerializer(instance=act_list, many=True).data
            ret['code'] = 2000
            ret['message'] = "工作人员获取"
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

    def get(self, request, *args, **kwargs):
        ret = {}
        # user = request.user
        user = User.objects.get(username="19510146")
        perms = user.get_all_permissions()
        
        manage_pers = []
        for i in perms:
            if i.find('manage') > 0:
                manage_pers.append(i[i.find('-')+1:])

        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)
