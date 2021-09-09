'''
Author: 邹洋
Date: 2021-09-08 19:34:17
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-09 08:22:21
Description: 
'''
from django.contrib import admin
from .models import *

@admin.register(Floor)
class Floor(admin.ModelAdmin):
    list_display = (
        "id", "building", "name", "is_open"
    )
@admin.register(Room)
class Room(admin.ModelAdmin):
    list_display = (
        "id", "floor", "name", 
    )
@admin.register(StuInRoom)
class StuInRoom(admin.ModelAdmin):
    list_display = (
        "id", "room","user", "user_name",'bed_position'
    )
    list_filter = ("room__floor__building__name","room__floor__name","room__name",)
     # 增加自定义按钮

