'''
Author: 邹洋
Date: 2022-02-06 21:56:58
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-06 21:56:58
Description: 
'''
from django.middleware.common import MiddlewareMixin

from Core.utils import push_wx

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
