"""用户操作"""
import hashlib
import requests
import time
from django.contrib.auth import authenticate
from Apps.User.models import Tpost, Token
from Apps.User.utils import auth
from Apps.User.utils.exceptions import *


def get_openid(js_code):
    """
    js_code : 微信客户端发送过来的标识
    根据js_code获取微信唯一标识
    """
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    data = {
        'appid': 'wx9a63d4bc0c3480f3',
        'secret': 'e8f66b9581ced527fb319c015e670044',
        'js_code': js_code
    }
    ret = requests.get(url, params=data)  # 发get请求
    try:
        openid = ret.json()['openid']
        return openid
    except KeyError:
        print('请检查 appid-secret 是否正确')
        return False


class UserExtraOperate(object):
    """用户额外登录等操作"""

    def __init__(self, request):
        self._request = request
        self._user = request.user

    def login(self, login_type):
        login_type = str(login_type).strip()
        if login_type == 'wx':
            return self.__wx_login()
        elif login_type == 'web':
            return self.__web_login()
        else:
            # 参数错误
            raise ParamException("参数有误")

    def __wx_login(self):
        js_code = self._request.data['js_code']
        open_id = get_openid(js_code)
        if not open_id:
            # 获取openid失败
            raise VxAuthException("获取openid失败")
        try:
            user = Tpost.objects.get(wx_openid=open_id).user
            token = auth.update_token(user)
            return token
        except Tpost.DoesNotExist:
            # 微信未绑定
            raise VxBindException("微信未绑定")

    def __web_login(self):
        __username = self._request.data.get('username', None)
        __password = self._request.data.get('password', None)
        if __username and __password:
            __user = authenticate(username=__username, password=__password)
            if __user:
                __token = auth.update_token(__user)
                return __token
            raise False
        # 参数缺失
        raise ParamException("参数缺失: 获取用户名密码失败")

    def register(self):
        __username = self._request.data.get('username', None)
        __password = self._request.data.get('password', None)
        __repeat_password = self._request.data.get('repeat_password', None)
        # 确认密码由前端验证(这点小事还放后端?)
        if __username and __password and __repeat_password and __password == __repeat_password:
            __user = auth.models.User.objects.create_user(username=__username)
            __user.set_password(__password)
            __user.save()
            return True
        # 参数缺失
        raise ParamException("没有获取到用户名,密码等参数")
