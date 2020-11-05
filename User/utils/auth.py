from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from User import models
import json
import os
import time
class TokenAuth(BaseAuthentication):
    def authenticate(self,request):
        #判断是否在headers携带token
        token = request.META.get("HTTP_TOKEN")
        # token = request._request.GET.get('token')
        TokenObj = models.User_Token.objects.filter(token = token).first()
        if not TokenObj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        #在rest 内部会把他们给request
        return (TokenObj.user,TokenObj)
    def authenticate_header(self,request):
        pass



def getToken(request):
     return request.META.get("HTTP_TOKEN")

def getUser(request):
    try:
        token = getToken(request)
        Obj = models.User_Token.objects.filter(
                    token=token).first()
        return Obj.user
    except:
        return


def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

def updateToken(User_AccountObj, token):
    TokenObj = models.Token.objects.filter(user_id=User_AccountObj).first()
    if not TokenObj:
        models.Token.objects.create(user_id=User_AccountObj, token=token)
    else:
        models.Token.objects.filter(
            user_id=User_AccountObj).update(token=token)