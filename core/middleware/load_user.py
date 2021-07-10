'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors: OBKoro1
LastEditTime: 2021-07-04 14:15:44
Description: 中间件
'''
from django.utils.deprecation import MiddlewareMixin
from Apps.User import models

class LoadUserObject(MiddlewareMixin):
    """
    中间件实现
    加载当前用户对象
    封装到Request请求里面
    如果没有就 request.user_object = None
    并且向下层传递
    """

    def process_request(self, request):
        token = request.META.get("HTTP_TOKEN")
        token = models.Token.objects.filter(token=token).first()
        if not token:
            request.is_user = False
            return
        request.user = token.user
        username = request.user.username
        request.is_user = True
