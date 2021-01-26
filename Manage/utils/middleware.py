from django.utils.deprecation import MiddlewareMixin

class LoadUserObject(MiddlewareMixin): 
    '''
    加载user对象
    传递给下层
    '''
    def process_request(self, request):
        request.get_user = "当前用户:XXX"
        print("加载用户对象。") 