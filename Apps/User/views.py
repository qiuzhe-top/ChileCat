# import random
# import string
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import requests
from Apps.User.utils.auth import update_token,get_user,get_token
from . import models,ser
from django.contrib.auth.models import User
from .utils.auth import get_groups
from django.contrib.auth import authenticate
from Apps.Permission.utils.auth import AuthPer
def get_openid(js_code):    
    '''
    js_code : 微信客户端发送过来的标识
    根据js_code获取微信唯一标识
    '''
    url='https://api.weixin.qq.com/sns/jscode2session'
    data = {
        'appid':'wx9a63d4bc0c3480f3',
        'secret':'e8f66b9581ced527fb319c015e670044',
        'js_code':js_code
        }
    ret =  requests.get(url,params=data) #发get请求
    try:
        openid = ret.json()['openid']
        return openid
    except KeyError:
        print('请检查 appid-secret 是否正确')
        return None
# from .models import Tpost
class Auth(APIView):
    '''
    Auth
    '''
    API_PERMISSIONS = ['用户','get','post','delete','put']
    def post(self, request):
        '''
        post method
        '''
        ret = {}
        try:
            login_type = request.data['type']
        except KeyError as req_failed:
            ret['code']=5000
            ret['message']='缺少参数：'+str(req_failed)
            return JsonResponse(ret)

        if login_type == 'wx':
            self.wx_login(request,ret)
        elif login_type == 'web':
            self.web_login(request,ret)
        else:
            ret['code']=5000
            ret['message']='参数异常：' + login_type
            return JsonResponse(ret)

        return JsonResponse(ret)

    def delete(self, request):
        """
        doc string
        """
        ret = {'code':2000,'message':"执行成功",'data':{}}
        return JsonResponse(ret)
    
    def put(self, request):
        '''
        注册账户
        '''
        ret = {}

        try:
            username = request.data['username']
            password = request.data['password']
            repeat_password = request.data['repeat_password']
        except KeyError as req_failed:
            ret['code']=5000
            ret['message']='缺少参数：'+str(req_failed)
            return JsonResponse(ret)

        if  password != repeat_password:
            ret['code']=5000
            ret['message']='两次密码不一致'
            return JsonResponse(ret)

        user = User.objects.create_user(username, '', password)
        if user:
            ret['code']=2000
            ret['message']='创建成功'
            return JsonResponse(ret)

        ret['code']=5000
        ret['message']='创建失败'
        return JsonResponse(ret)


    def wx_login(self,request,ret):
        '''
        微信登录
        '''
        print(request.data)
        js_code = request.data['js_code']
        open_id = get_openid(js_code)

        if open_id is None:
            ret['code'] = '5000'
            ret['message'] = '微信验证失败'
            return JsonResponse(ret)

        try:
            user = models.Tpost.objects.get(wx_openid = open_id).user
            token = update_token(user)
            ret['code'] = 2000
            ret['message'] = '登陆成功'
            ret['data'] = {'token':token}
        except models.Tpost.DoesNotExist:
            ret['code'] = 5001
            ret['message'] = '用户未绑定'
            
        return JsonResponse(ret)
    
    def web_login(self,request,ret):
        '''
        平台账户登录
        获取账号密码
        验证账户密码
        返回token或错误
        DJanog rest_framework jwt 登录
        '''
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError as req_failed:
            ret['code']=5000
            ret['message']='缺少参数：'+str(req_failed)
            return JsonResponse(ret)

        user = authenticate(username=username,password=password)
        if user:
            token = update_token(user)
            ret['code'] = 2000
            ret['data'] = {'token':token}
        else:
            ret['code'] = 5000
            ret['message'] = "账号或密码错误"
        return JsonResponse(ret)

# 获取个人信息
class Information(APIView):
    
    # authentication_classes = [AuthPer,]
    API_PERMISSIONS = ['获取个人信息','get']
    '''
    Information
    '''
    def get(self, request):
        '''
        get method
        获取用户
        获取用户信息
        返回信息
        '''
        ret = {'code':2000,'message':"执行成功",'data':{}}
        user = request.user
        data = {}
        p = request.user.get_all_permissions()
        data['permissions'] = [x[11:] for x in p if x.find('OPERATE')!= -1]
        data['roles']= get_groups(request)
        data['introduction'] = 'I am a super administrator'
        data['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
        data['name'] = user.userinfo.name
        try:
            data['grade'] = user.studentinfo.grade_id.name
        except:
            data['grade'] = ''
        ret['data'] = data
        return JsonResponse(ret)

class ClassList(APIView):
    '''关联班级'''
    def get(self, request):
        '''关联班级'''
        ret = {}
        user = get_user(request)
        info = user.userinfo
        ser_list = ''
        if info.identity=="student":
            grade = user.studentinfo.grade_id
            # django 序列化
            ser_list = ser.GradeSerializer(instance=grade,many=False).data
        elif info.identity=="teacher":
            grade = user.teacherforgrade_set.all()
            ser_list = ser.TeacherForGradeSerializer(instance=grade,many=True).data
        elif info.identity=="college":
            college_list = user.teacherforcollege_set.all()
            ser_list = ser.TeacherForCollegeSerializer(instance=college_list,many=True).data
            ser_all_class = []
            for item in ser_list:
                for k,v in item.items():
                    ser_all_class += v
            ser_list = ser_all_class
        if len(ser_list) == 0:
            ret['code'] = 5000
            ret['message']= "您的班级未绑定，请联系管理员"
            return JsonResponse(ret)
        ret['code'] = 2000
        ret['message'] = "执行成功"
        ret['data'] = ser_list
        return JsonResponse(ret)

# 绑定微信
class Bindwx(APIView):
    '''
    绑定微信
    '''
    API_PERMISSIONS = ['绑定微信','post']
    def post(self, request):
        '''
        post method
        '''
        ret = {}

        try:
            js_code  = request.data['js_code']
            username = request.data['username']
            password = request.data['password']
            print(js_code,username,password)
        except KeyError:
            ret['code'] = 5000
            ret['message'] = "请求数据异常"
            return JsonResponse(ret)


        user = authenticate(username=username,password=password)
        if user:
            token = update_token(user)
            ret['data'] = {'token':token}
        else:
            ret['code'] = 5000
            ret['message'] = "账号或密码错误"
            return JsonResponse(ret)


        try:
            old_openid = user.tpost.wx_openid
            if old_openid:
                # print(old_openid)
                ret['code'] = 5000
                ret['message'] = "请勿重新绑定"
                return JsonResponse(ret)
        except:
            pass


        openid = get_openid(js_code)
        if openid is None:
            ret['code'] = 5000
            ret['message'] = "微信用户异常"
            return JsonResponse(ret)

        tpost,b = models.Tpost.objects.get_or_create(user=user)

        if tpost.wx_openid:
            ret['code'] = 5000
            ret['message'] = "请勿重新绑定"
            return JsonResponse(ret)

        tpost.wx_openid = openid
        tpost.save()

        ret['message'] = '绑定成功'
        ret['code'] = 2000
        return JsonResponse(ret)

class MoodManage(APIView):
    '''心情监测'''
    def post(self, request):
        '''心情监测'''
        ret = {}
        mod_level = request.data.get('mod_level')
        message =   request.data.get('message')
        print(mod_level,message)
        user = get_user(request)
        grade = user.studentinfo.grade_id
        print(mod_level,message,user,grade)

        dic = {
            'user':user,
            'Grade':grade,
            'message':message,
            'mod_level':mod_level
        }
        models.UserMood.objects.create(**dic)
        ret['message'] = '发送成功'
        ret['code'] = 2000
        return JsonResponse(ret)
