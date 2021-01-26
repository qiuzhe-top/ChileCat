from rest_framework.permissions import BasePermission

# API接口权限
class ApiPermission(BasePermission):
    message = '访问接口失败'

    def has_permission(self, request, view):
        """
        只有拥有当前api权限的用户通过
        """
        print("接口权限：只有拥有当前api权限的用户通过")
        # user [2,34,5,6]
        # url [2,3]
        # if 在不在 API权限 (ApiPer)
        if 1==11:
          return True
        else:
          return False