'''
views
'''
import random
import string
from rest_framework.views import APIView
from django.http import JsonResponse
import requests
from User.utils.auth import md5,update_token,get_user
from . import models,ser
# 微信登录
def get_openid(js_code):
    '''
    根据jscode获取微信唯一标识
    '''
    url='https://api.weixin.qq.com/sns/jscode2session'
    data = {
        'appid':'wx9a63d4bc0c3480f3',
        'secret':'caaf6191b5c51021a7839197780862ec',
        'js_code':js_code
        }
    ret = requests.get(url,params=data) #发get请求
    try:
        openid = ret.json()['openid']
        return openid
    except:
        #print('获取openid失败')
        return None
def wx_login(request,ret):
    '''
        判断登录类型
            微信登录
                获取openid
                not 通过oid查找token表是否对应有用户：
                    创建新的用户进行保存
                    创建token
                else
                    更新token
                    返回token
    '''
    js_code = request.data['js_code']
    open_id = get_openid(js_code)
    if open_id is None:
        ret['code'] = '4000'
        ret['message'] = '验证失败'
        return JsonResponse(ret)
    token = models.Token.objects.filter(wx_openid = open_id)
    user = None
    if len(token)==0:
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        dic = {
            'user_name':ran_str,
            'pass_word':ran_str
        }

        user = models.User.objects.create(**dic)
        dic2 = {
            'token':md5(ran_str),
            'wx_openid':open_id,
            'user_id':user
        }
        ret['data'] = {'token':dic2['token']}
        #print(dic2)
        models.Token.objects.create(**dic2)
    else:
        user = token[0].user_id
        #print(user.id)
        ret['data']= {'token':md5(open_id)}
        update_token(user,ret['data']['token'])
# 后台登录
def admin_login(request,ret):
    '''
    获取账号密码
    验证账户密码
    返回token或错误
    '''
    username = request.data['username']
    password = request.data['password']
    user = models.User.objects.filter(user_name = username).first()
    if user:
        if password == user.pass_word:
            token = md5(user)
            update_token(user,token)
            ret['data']['token'] = token
            return JsonResponse(ret)
    ret['message']='登录失败'
    ret['code']=5000
    # 1
    
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
        ret['data'] = data
        return JsonResponse(ret)
# 关联班级
class ClassList(APIView):
    def get(self, request, *args, **kwargs):
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'

        user = get_user(request)
        info = user.userinfo
        if info.identity=="student":
            grade = user.studentinfo.grade_id
            # django 序列化
            ret['data'] = ser.GradeSerializer(instance=grade,many=False).data
            return JsonResponse(ret)
        elif info.identity=="teacher":
            grade = user.teacherforgrade_set.all()
            ret['data'] = ser.TeacherForGradeSerializer(instance=grade,many=True).data
            return JsonResponse(ret)
        elif info.identity=="college":
            grade = user.teacherforcollege_set.all()
            ret['data'] = ser.TeacherForCollegeSerializer(instance=grade,many=True).data
            return JsonResponse(ret)

        return JsonResponse(ret)
    def post(self, request, *args, **kwargs):
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)
    def put(self, request, *args, **kwargs):
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)
    def delete(self, request, *args, **kwargs):
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)
