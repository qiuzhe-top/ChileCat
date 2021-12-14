'''
Author: 邹洋
Date: 2021-12-14 11:31:14
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-12-14 12:07:30
Description: 全局异常
'''
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.middleware.common import MiddlewareMixin

from core.push_plus import push_wx



class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        :return:
        """
        # 异常处理
        push_wx('异常捕获',exception)
        return None

