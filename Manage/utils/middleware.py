from django.utils.deprecation import MiddlewareMixin

class LoadUserObject(MiddlewareMixin): 
    '''
    中间件实现
    加载当前用户对象
    封装到Request请求里面
    如果没有就 request.user_object = False  
    并且向下层传递
    '''
    def process_request(self, request):
        request.user_object = "Administrator"
        # print("中间件: 加载用户对象。") 