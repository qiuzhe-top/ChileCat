from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from Apps.Activity.models import Manage


class AttendancePermission(BasePermission):
    """
    活动控制
    针对活动管理表内的一条数据是否有权限操作
    """

    def has_permission(self, request, view):
      try:
        id = request.data['id']
        perms = request.user.get_all_permissions()
        code_name = Manage.objects.get(id=id).code_name
        for perm in perms:
          if perm.find(code_name) > 0:
              return True
        return False
      except:
        return False