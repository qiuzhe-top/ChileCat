from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
import requests
from . import models
from User.utils.auth import md5,updateToken
import random
import string
# 根据jscode获取微信唯一标识
def get_openid(js_code):
    url='https://api.weixin.qq.com/sns/jscode2session'
    data = {'appid':'wx9a63d4bc0c3480f3','secret':'caaf6191b5c51021a7839197780862ec','js_code':js_code}
    r = requests.get(url,params=data) #发get请求
    try:
        openid = r.json()['openid']
        return openid
    except:
        print('获取openid失败')
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
    if open_id == None:
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
        print(dic2)
        models.Token.objects.create(**dic2)
    else:
        user = token[0].user_id
        print(user.id)
        ret['data']= {'token':md5(open_id)}
        updateToken(user,ret['data']['token'])
class Auth(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code':2000,'message':"执行成功",'data':{}}
 
        type = request.data['type']
        if type == 'wx':
            wx_login(request,ret)
        return JsonResponse(ret)

    def get(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def put(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)

    def delete(self, request):
        ret = {}
        ret['code'] = '2000'
        ret['message'] = '提示信息'
        ret['data'] = 'data'
        return JsonResponse(ret)
