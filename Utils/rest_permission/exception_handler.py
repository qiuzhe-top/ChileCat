from rest_framework.views import exception_handler

# 自定义认证错误时的返回格式
def custom_exception_handler(exc, context):
    
    response = exception_handler(exc, context)
    if response is not None:
        response.data['code'] = 5500 if (
                response.data['detail'] == '用户认证失败'
        ) else (
            response.status_code
        )
        response.data['message'] = response.data['detail']
        del response.data['detail']  # 删除detail字段
    return response
