"""用户模块"""
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.http import JsonResponse
from . import models, ser
from django.contrib.auth.models import User
from .utils.auth import get_groups
from Apps.User.models import StudentInfo, TeacherForGrade
from Apps.User.utils.user import UserExtraOperate
from Apps.User.utils.exceptions import *
from django.contrib.auth.models import Permission,AnonymousUser
from Manage.models_extension.models_permission import ApiPermission

from django.contrib.contenttypes.models import ContentType
from Apps.User.utils import auth


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
            if 5506 == token:
                ret['data'] = token
                ret['message'] = "第一次登陆请修改密码"
                ret['code'] = token
            else:
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

    def put(self,request):
        '''修改密码
            request:
                password
                password_repeat
        '''
        ret = {}
        
        user = request.user
        password_new = request.data['password_new']
        password_repeat = request.data['password_repeat']
        if user == AnonymousUser:
            username = request.data['username']
            password_old = request.data['password_old']
            user = authenticate(username=username, password=password_old)
    
        if password_new == password_repeat and len(password_new)>=6 and user:
            user.set_password(password_new)
            user.save()
            auth.update_token(user)
            ret['message'] = '修改成功'
            ret['code'] =  2000
        else:
            ret['message'] = '修改失败'
            ret['code'] =  5000

        return JsonResponse(ret)


    # def post(self, request):
    #     """
    #     注册账户
    #     """
    #     ret = {'code': 0000, 'message': ""}
    #     try:
    #         user = UserExtraOperate(self.request)
    #         user.register()
    #         ret['message'] = "注册成功"
    #         ret['code'] = 2000
    #     except ParamException as leak_param:
    #         ret['message'] = str(leak_param)
    #         ret['code'] = 5000
    #     return JsonResponse(ret)

    def delete(self, request):
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
        user = self.request.user
        data = {'permissions': []}
        
        p = self.request.user.user_permissions.filter().exclude(
            content_type=ContentType.objects.get_for_model(ApiPermission)
        ).values()

        # TODO 模型发生变化 operatepermission 失效
        for permission in p:
            if "operatepermission" not in permission['codename']:
                data['permissions'].append(permission['codename'])
                
        data['roles'] = get_groups(request)
        data['introduction'] = 'I am a super administrator'
        data['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'

        try:
            data['name'] = user.userinfo.name
        except:
            ret['code'] = 5000
            ret['message'] = '用户信息不完整'
            return JsonResponse(ret)

        data['is_admin'] = request.user.is_staff
        data['is_superuser'] = request.user.is_superuser
        try:
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
        
        try:
            info = user.userinfo
        except:
            ret['code'] = 5000
            ret['message'] = '用户信息不完整'
            return JsonResponse(ret)

        try:
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
        except:
            ret['code'] = 5000
            ret['message'] = "未知班级信息"
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
