'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-11 16:20:57
Description: 
'''
from django.contrib import admin

from .models import *


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """任务管理"""
    list_display = (
        "id", "college", "types", "is_open"
    )
    filter_horizontal = ("admin","buildings","grades")
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """考勤记录"""
    list_display = (
        "id", "task","rule_str","score","grade_str","room_str","student_approved","student_approved_name","worker","worker_name","manager","star_time"
    )
    list_filter = ("rule__rule__name","rule__name","grade_str")

    date_hierarchy = 'star_time'

    search_fields = ("student_approved__username","student_approved__name")

    def  student_approved_name(self,obj):
        try:
            return obj.student_approved.name
        except:
            return None
    student_approved_name.short_description = '被执行者姓名'

    def  worker_name(self,obj):
        try:
            return obj.worker.name
        except:
            return None
    worker_name.short_description = '执行者姓名'

@admin.register(RuleDetails)
class RuleDetailsAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name","score","rule","parent_id"
    )
