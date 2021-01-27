'''管理视图'''
from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.

class Test(APIView):
    '''后台接口调用'''
    def get(self,request):
        return JsonResponse({"1":"1"})
