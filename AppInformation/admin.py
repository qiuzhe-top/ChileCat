'''
Author: 邹洋
Date: 2022-02-07 11:26:10
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-23 10:58:52
Description: 
'''
from django.contrib import admin
from django.http import JsonResponse

from Core.common.excel import ExcelBase
from .models import *
# Register your models here.

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "id", "college","college"
    )
@admin.register(StuInRoom)
class StuInRoomAdmin(admin.ModelAdmin):
    list_display = (
        "id", "room","user","user_name","bed_position","is_active"
    )
    def user_name(self,obj):
        return obj.user.name

    user_name.short_description = '姓名'

    search_fields = ("room__id","user__username","user__name")
    list_editable = ('bed_position','is_active')
