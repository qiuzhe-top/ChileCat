"""用户操作"""
import requests
from django.contrib.auth import authenticate
from Apps.User.models import Tpost, User
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
        self._user = self._request.user

    def login(self, login_type):
        __login_type = str(login_type).strip()
        if __login_type == 'wx':
            return VxLogin(self._request).login()
        elif __login_type == 'web':
            return WebLogin(self._request).login()
        else:
            raise ParamException("参数有误")

    # def __wx_login(self):
    #     js_code = self._request.data['js_code']
    #     open_id = get_openid(js_code)
    #     if not open_id:
    #         # 获取openid失败
    #         raise VxAuthException("获取openid失败")
    #     try:
    #         user = Tpost.objects.get(wx_openid=open_id).user
    #         token = auth.update_token(user)
    #         return token
    #     except Tpost.DoesNotExist:
    #         # 微信未绑定
    #         raise VxBindException("微信未绑定")
    #
    # def __web_login(self):
    #     __username = self._request.data.get('username', None)
    #     __password = self._request.data.get('password', None)
    #     if __username and __password:
    #         __user = authenticate(username=__username, password=__password)
    #         if __user:
    #             __token = auth.update_token(__user)
    #             return __token
    #         raise False
    #     # 参数缺失
    #     raise ParamException("参数缺失: 获取用户名密码失败")

    def register(self):
        __username = self._request.data.get('username', None)
        __password = self._request.data.get('password', None)
        __repeat_password = self._request.data.get('repeat_password', None)
        if __username and __password and __repeat_password and __password == __repeat_password:
            __user = auth.models.User.objects.create_user(username=__username)
            __user.set_password(__password)
            __user.save()
            return True
        raise ParamException("没有获取到用户名,密码等参数")

    def vx_bind(self):
        VxBind(self._request).bind()


class VxBind(object):
    def __init__(self, request):
        self.__request = request

    def bind(self):
        __token = ""
        try:
            js_code = self.__request.data['js_code']
            username = self.__request.data['username']
            password = self.__request.data['password']
            print(js_code, username, password)
        except KeyError as leak_param:
            return leak_param
        user = authenticate(username=username, password=password)
        if user:
            __token = auth.update_token(user)
        else:
            return LoginExcept("用户不存在")
        old_openid = None
        try:

            tpost = Tpost.objects.get(user=user)
            old_openid = tpost.wx_openid
        except Tpost.DoesNotExist:
            old_openid = None
        if old_openid:
            # print(old_openid)
            raise VxBindException("请勿重新绑定")
        openid = get_openid(js_code)
        if openid is None:
            raise VxBindException("微信用户异常")

        tpost, b = Tpost.objects.get_or_create(user=user)

        if tpost.wx_openid:
            return VxBindException("请勿重新绑定")
        tpost.wx_openid = openid
        tpost.save()
        return __token


class Login(object):
    def __init__(self, request):
        self._request = request

    def login(self):
        pass


class VxLogin(Login):
    def __init__(self, request):
        super().__init__(request)
        self.__request = request

    def login(self):
        __js_code = self.__request.data['js_code']
        __open_id = get_openid(__js_code)
        if not __open_id:
            # 获取openid失败
            raise VxAuthException("获取openid失败")
        try:
            __user = Tpost.objects.get(wx_openid=__open_id).user
            __token = auth.update_token(__user)
            return __token
        except Tpost.DoesNotExist:
            raise VxBindException("微信未绑定")


class WebLogin(Login):
    def __init__(self, request):
        super().__init__(request)
        self.__request = request

    def login(self):
        __username = self.__request.data.get('username', None)
        __password = self.__request.data.get('password', None)
        if __username and __password:
            __user = authenticate(username=__username, password=__password)
            if __user:
                __token = auth.update_token(__user)
                return __token
            raise WebLoginException("登录失败: 账号密码错误")
        # 参数缺失
        raise ParamException("参数缺失: 获取用户名密码失败")
