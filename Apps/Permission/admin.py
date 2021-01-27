'''把数据注册到admin网站'''
from django.contrib import admin
from .models import Role,Permission,ApiPermission,ElementPermission,OperatePermission
from django.utils.html import format_html
# Register your models here.

@admin.register(Role)
class RoleTeleAdmin(admin.ModelAdmin):
    '''角色'''
    def role_to_permit(self,obj):
        per_count = obj.role_permit.count()
        if per_count:
            return "该用户有"+str(per_count)+"项权限"
        return format_html('<span style="color:#8E8E8E;">(该角色无权限)</span>')
    list_display = ("id","name","role_to_permit")
    # autocomplete_fields = ['role_permit']
    filter_horizontal = ['role_permit']
    role_to_permit.short_description = "角色权限"
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
