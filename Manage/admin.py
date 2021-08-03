'''
Author: your name
Date: 2021-07-13 17:37:04
LastEditTime: 2021-08-03 08:28:19
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \ChileCat\Manage\admin.py
'''

'''把数据注册到admin网站'''
from django.contrib import admin
from django.utils.html import format_html
from .models import ApiPermission,ElementPermission,OperatePermission

# @admin.register(ApiPermission)
# class ApiPermissionTeleAdmin(admin.ModelAdmin):
#     '''接口访问'''
#     def codename(self,obj):
#         return obj.permission.codename
        
#     list_display = ("id","codename","permission",'is_verify')
#     list_filter = ('is_verify', ) 

# @admin.register(ElementPermission)
# class ElementPermissionTeleAdmin(admin.ModelAdmin):
#     '''元素访问'''
#     list_display = ("id","name","per_id")


# @admin.register(OperatePermission)
# class OperatePermissionTeleAdmin(admin.ModelAdmin):
#     '''操作'''
#     list_display = ("id","permission")
