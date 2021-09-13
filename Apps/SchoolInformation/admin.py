'''
Author: 邹洋
Date: 2021-09-08 19:34:17
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-10 18:26:51
Description: 
'''
from django.contrib import admin
from django.http.response import JsonResponse
from simpleui.admin import AjaxAdmin

from .models import *


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = (
        "id", "building", "name", "is_open"
    )
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id", "floor", "name", 
    )

from django.http import HttpResponse


@admin.register(StuInRoom)
class StuInRoomAdmin(AjaxAdmin):
    list_display = (
        "id", "room","user", "user_name",'bed_position'
    )
    list_filter = ("room__floor__building__name","room__floor__name","room__name",)
     # 增加自定义按钮
    list_per_page = 20
    actions = ('upload_file',)

    def upload_file(self, request, queryset):
        # 这里的upload 就是和params中配置的key一样
        upload= request.FILES
        
        print(upload)
        return JsonResponse(data={
                'status': 'error',
                'msg': '请先选中数据！'
            })


    upload_file.short_description = '文件上传对话框'
    upload_file.type = 'success'
    upload_file.icon = 'el-icon-upload'
    upload_file.enable = True

    upload_file.layer = {
        'params': [{
            'type': 'file',
            'key': 'upload',
            'label': '文件'
        },{
            'type': 'number',
            'key': 'money',
            'label': '金额',
            # 设置默认值
            'value': 1000
        }]
    }
