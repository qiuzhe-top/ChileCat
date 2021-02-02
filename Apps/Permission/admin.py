'''把数据注册到admin网站'''
from django.contrib import admin
from django.utils.html import format_html
from .models import Role,Permission,ApiPermission,ElementPermission,OperatePermission
# Register your models here.

@admin.register(Role)
class RoleTeleAdmin(admin.ModelAdmin):
    '''角色'''
    def role_to_permit(self,obj):
        '''个性化角色权限'''
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
    def show_des(self,obj):
        '''个性化权限的描述'''
        if obj.description == "" or obj.description is None:
            return format_html('<span style="color:#8E8E8E;">(没有描述)</span>')
        return obj.description
    list_display = ("id","name","per_type","show_des")
    show_des.short_description = "描述"
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
