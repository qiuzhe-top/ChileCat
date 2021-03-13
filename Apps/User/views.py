"""用户模块"""
from rest_framework.views import APIView
from django.http import JsonResponse
from . import models, ser
from django.contrib.auth.models import User
from .utils.auth import get_groups
from Apps.User.models import StudentInfo, TeacherForGrade
from Apps.User.utils.user import UserExtraOperate
from Apps.User.utils.exceptions import *
from django.contrib.auth.models import Permission
from Apps.Permission.models import OperatePermission
from django.contrib.contenttypes.models import ContentType


class Auth(APIView):
    """
    登录和注册
    """

    API_PERMISSIONS = ['用户Auth', 'post', 'delete', 'put']

    def post(self, request):
        """
        登录
        """
        ret = {'code': 0000, 'message': "", 'data': {'token': ""}}
        login_type = self.request.data.get('type', None)
        user = UserExtraOperate(self.request)
        try:
            token = user.login(login_type)
            ret['data']['token'] = token
            ret['message'] = "获取成功"
            ret['code'] = 2000
        except VxBindException as not_bind:
            ret['message'] = str(not_bind)
            ret['code'] = 5001
        except VxAuthException as auth_filed:
            ret['message'] = str(auth_filed)
            ret['code'] = 5000
        except WebLoginException as web_failed:
            ret['message'] = str(web_failed)
            ret['code'] = 5000
        except ParamException as leak_param:
            ret['message'] = str(leak_param)
            ret['code'] = 5000
        return JsonResponse(ret)

    def put(self, request):
        """
        注册账户
        """
        ret = {'code': 0000, 'message': ""}
        try:
            user = UserExtraOperate(self.request)
            user.register()
            ret['message'] = "注册成功"
            ret['code'] = 2000
        except ParamException as leak_param:
            ret['message'] = str(leak_param)
            ret['code'] = 5000
        return JsonResponse(ret)

    def delete(self,request):
        ret = {'code': 2000}
        return JsonResponse(ret)


class Information(APIView):
    """获取个人信息"""

    API_PERMISSIONS = ['获取个人信息', '*get']
    '''
    Information
    '''

    def get(self, request):
        """
        get method
        获取用户
        获取用户信息
        返回信息
        """
        ret = {'code': 2000, 'message': "执行成功", 'data': {}}

        try:
            user = self.request.user
            data = {'permissions': []}
            p = self.request.user.user_permissions.filter(
                content_type=ContentType.objects.get_for_model(OperatePermission)).values()
            for permission in p:
                if "operatepermission" not in permission['codename']:
                    data['permissions'].append(permission['codename'])
            data['roles'] = get_groups(request)
            data['introduction'] = 'I am a super administrator'
            data['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
            data['name'] = user.userinfo.name
            data['is_admin'] = request.user.is_staff
            data['is_superuser'] = request.user.is_superuser
            data['grade'] = StudentInfo.objects.get(user=self.request.user).grade.name \
                if StudentInfo.objects.filter(user=self.request.user).exists() \
                else "该用户无班级"
            ret['data'] = data
        except StudentInfo.DoesNotExist:
            data['grade'] = ''
        return JsonResponse(ret)


class ClassList(APIView):
    """关联班级"""

    API_PERMISSIONS = ['关联班级', '*get']

    def get(self, request):
        """关联班级"""
        ret = {}
        user = self.request.user
        info = user.userinfo
        ser_list = ''
        if info.identity == "student":
            grade = user.studentinfo.grade
            # django 序列化
            ser_list = ser.GradeSerializer(instance=grade, many=False).data
        elif info.identity == "teacher":
            grade = TeacherForGrade.objects.filter(user_id=self.request.user)
            ser_list = ser.TeacherForGradeSerializer(instance=grade, many=True).data
        elif info.identity == "college":
            college_list = user.teacherforcollege_set.all()
            ser_list = ser.TeacherForCollegeSerializer(instance=college_list, many=True).data
            ser_all_class = []
            for item in ser_list:
                for k, v in item.items():
                    ser_all_class += v
            ser_list = ser_all_class
        if len(ser_list) == 0:
            ret['code'] = 5000
            ret['message'] = "您的班级未绑定，请联系管理员"
            return JsonResponse(ret)
        ret['code'] = 2000
        ret['message'] = "执行成功"
        ret['data'] = ser_list
        return JsonResponse(ret)


# 绑定微信
class BindVx(APIView):
    """
    绑定微信
    """
    API_PERMISSIONS = ['绑定微信', '*post']

    def post(self, request):
        """
        微信绑定
        """
        ret = {'code': 0000, 'message': "", 'data': {'token': ""}}
        try:
            print("绑定微信界面")
            ret['data']['token'] = UserExtraOperate(self.request).vx_bind()
            ret['code'] = 2000
            ret['message'] = "绑定成功"
        except VxBindException as bind_failed:
            ret['code'] = 5000
            ret['message'] = str(bind_failed)
        return JsonResponse(ret)


class MoodManage(APIView):
    """心情监测"""
    API_PERMISSIONS = ['心情监测','*post']
    def post(self, request):
        """心情监测"""
        ret = {}
        mod_level = self.request.data.get('mod_level')
        message = self.request.data.get('message')
        print(mod_level, message)
        user = self.request.user
        grade = user.studentinfo.grade
        print(mod_level, message, user, grade)
        dic = {
            'user': user,
            'Grade': grade,
            'message': message,
            'mod_level': mod_level
        }
        models.UserMood.objects.create(**dic)
        ret['message'] = '发送成功'
        ret['code'] = 2000
        print(ret)
        return JsonResponse(ret)

class Activeity(APIView):

    API_PERMISSIONS = ['活动','get']
    def get(self, request, *args, **kwargs):
        ret = {}
        id = request.GET.get('id',None)

        if id:
            obj = models.Activity.objects.get(id = id)
            data = ser.ActiveitySerializer(instance=obj,many=False).data
            ret['code'] = 2000
            ret['data'] = data
            return JsonResponse(ret)

        act_list = models.Activity.objects.all()
        datas = ser.ActiveitySerializer(instance=act_list,many=True).data
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = datas
        return JsonResponse(ret)