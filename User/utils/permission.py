'''
#
'''
from rest_framework.permissions import BasePermission
class CadrePermission(BasePermission):
    '''
    /
    '''
    def has_permission(self,request,view):
        if request.user.role == "cadre":
            return True
        # print(request.user.role)
        return False
