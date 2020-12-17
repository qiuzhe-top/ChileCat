'''
views
'''
# import random
# import string
from rest_framework.views import APIView
from django.http import JsonResponse
import requests
from User.utils.auth import update_token,get_user
from . import models,ser
# 微信登录
def get_openid(js_code):
    '''
    根据jscode获取微信唯一标识
    '''
    url='https://api.weixin.qq.com/sns/jscode2session'
    data = {
        'appid':'wx9a63d4bc0c3480f3',
        'secret':'e8f66b9581ced527fb319c015e670044',
        'js_code':js_code
        }
    ret = requests.get(url,params=data) #发get请求
    print(ret.json())
    try:
        openid = ret.json()['openid']
        return openid
    except:
        print('y 请检查 appid-secret 是否正确')
        return None

def wx_login(request,ret):
    '''
    微信登录
    '''
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
    except:
        ret['code'] = 5001
        ret['message'] = '用户未绑定'
    return JsonResponse(ret)


    # token = models.Token.objects.filter(wx_openid = open_id)
    # user = None
    # if len(token)==0:
    #     ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    #     dic = {
    #         'user_name':ran_str,
    #         'pass_word':ran_str
    #     }

    #     user = models.User.objects.create(**dic)
    #     dic2 = {
    #         'token':md5(ran_str),
    #         'wx_openid':open_id,
    #         'user_id':user
    #     }
    #     ret['data'] = {'token':dic2['token']}
    #     #print(dic2)
    #     models.Token.objects.create(**dic2)
    # else:
    #     user = token[0].user_id
    #     #print(user.id)
    #     ret['data']= {'token':md5(open_id)}
    #     update_token(user,ret['data']['token'])
# 后台登录
def admin_login(request,ret):
    '''
    获取账号密码
    验证账户密码
    返回token或错误
    '''
    username = request.data['username']
    password = request.data['password']
    try:
        user = models.User.objects.get(user_name=username,pass_word=password)
        token = update_token(user)
        ret['data'] = {'token':token}
        return JsonResponse(ret)
    except:
        ret['code'] = 5000
        ret['message'] = "账号密码错误"
        return JsonResponse(ret)
    return JsonResponse(ret)

class Auth(APIView):
    '''
    Auth
    '''
    def post(self, request):
        '''
        post method
        '''
        ret = {'code':2000,'message':"执行成功",'data':{}}
        auth_type = request.data['type']
        if auth_type == 'wx':
            wx_login(request,ret)
        elif auth_type == 'admin':
            admin_login(request,ret)
        else:
            ret['code']=5000
            ret['message']='登录类型失败'
        return JsonResponse(ret)
    def delete(self, request):
        """
        docstring
        """
        ret = {'code':2000,'message':"执行成功",'data':{}}
        return JsonResponse(ret)
# 获取个人信息
class Information(APIView):
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
        user = get_user(request)
        data = {}
        data['roles']=['admin']
        data['introduction'] = 'I am a super administrator'
        data['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
        data['name'] = user.userinfo.name
        data['role'] = user.userinfo.identity
        ret['data'] = data
        return JsonResponse(ret)
# 关联班级
class ClassList(APIView):
    def get(self, request):
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
    def post(self, request):
        '''
        post method
        '''
        ret = {}

        try:
            js_code = request.data['js_code']
            username = request.data['username']
            password = request.data['password']
            print(js_code,username,password)
        except:
            ret['code'] = 5000
            ret['message'] = "请求数据异常"
            return JsonResponse(ret)

        user = None
        try:
            user = models.User.objects.get(user_name=username,pass_word=password)
            print(user)
        except:
            ret['code'] = 5000
            ret['message'] = "登录失败"
            return JsonResponse(ret)

        try:
            old_openid = user.tpost.wx_openid
            if old_openid:
                print(old_openid)
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

# 心情监测
class MoodManage(APIView):
    def post(self, request):
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

