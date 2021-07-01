
'''把数据注册到admin网站'''
from django.contrib import admin
from django.utils.html import format_html
from .models import ApiPermission,ElementPermission,OperatePermission

admin.site.site_header = "智服喵管理平台" 
@admin.register(ApiPermission)
class ApiPermissionTeleAdmin(admin.ModelAdmin):
    '''接口访问'''
    def codename(self,obj):
        return obj.permission.codename
        
    list_display = ("id","codename","permission",'is_verify')
    list_filter = ('is_verify', ) 

@admin.register(ElementPermission)
class ElementPermissionTeleAdmin(admin.ModelAdmin):
    '''元素访问'''
    list_display = ("id","name","per_id")


@admin.register(OperatePermission)
class OperatePermissionTeleAdmin(admin.ModelAdmin):
    '''操作'''
    list_display = ("id","permission")
