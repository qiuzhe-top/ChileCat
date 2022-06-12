'''
Author: 邹洋
Date: 2022-02-07 11:26:10
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-23 11:13:04
Description: 
'''
from django.contrib import admin
from django.conf import settings
from django.http import JsonResponse
from core.views import InitCacheConnection
from .models import *

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

    actions = ['enable_bedroom_choice','down_bedroom_choice']

    # 对话框 https://simpleui.72wo.com/docs/simpleui/QUICK.html#layer%E5%AF%B9%E8%AF%9D%E6%A1%86%E6%8C%89%E9%92%AE
    def enable_bedroom_choice(self, request, queryset):
        try:
            conn = InitCacheConnection()
            conn.cache.set('is_set_my_bedroom_number',1,60*60*24)
            return JsonResponse(data={
                'status': 'success',
                'msg': 'ok'
            })
        except:
             return JsonResponse(data={
                'status': 'error',
                'msg': 'error'
            })

    enable_bedroom_choice.short_description = '开启寝室选择'
    enable_bedroom_choice.type = 'success'

    def down_bedroom_choice(self, request, queryset):
        try:
            conn = InitCacheConnection()
            conn.cache.set('is_set_my_bedroom_number',1,1)
            return JsonResponse(data={
                'status': 'success',
                'msg': 'ok'
            })
        except:
             return JsonResponse(data={
                'status': 'error',
                'msg': 'error'
            })



    down_bedroom_choice.short_description = '关闭寝室选择'
    down_bedroom_choice.type = 'danger'