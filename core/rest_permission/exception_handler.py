'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors: OBKoro1
LastEditTime: 2021-07-04 14:09:53
Description: 权限认证错误时返回数据
'''
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    
    response = exception_handler(exc, context)
    if response is not None:
        response.data['code'] = 5500 if (
                response.data['detail'] == '用户认证失败'
        ) else (
            response.status_code
        )
        response.data['message'] = response.data['detail']
        del response.data['detail']
    return response
