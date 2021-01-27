'''把数据注册到admin网站'''
from django.contrib import admin
from .models import Role,Permission,ApiPermission,ElementPermission,OperatePermission
# Register your models here.

@admin.register(Role)
class RoleTeleAdmin(admin.ModelAdmin):
    '''角色'''
    list_display = ("id","name")
@admin.register(Permission)
class PeimissionTeleAdmin(admin.ModelAdmin):
    '''权限'''
    list_display = ("id","name","per_type","description")
@admin.register(ApiPermission)
class ApiPermissionTeleAdmin(admin.ModelAdmin):
    '''接口访问'''
    list_display = ("id","url","method","per_id")
@admin.register(ElementPermission)
class ElementPermissionTeleAdmin(admin.ModelAdmin):
    '''元素访问'''
    list_display = ("id","name","per_id")
@admin.register(OperatePermission)
class OperatePermissionTeleAdmin(admin.ModelAdmin):
    '''操作'''
    list_display = ("id","name","per_id")
