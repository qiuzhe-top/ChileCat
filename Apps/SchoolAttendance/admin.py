'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-12 11:51:05
Description: 
'''
# from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from .models import *
@admin.register(Task)
class Task(admin.ModelAdmin):
    """任务管理"""
    list_display = (
        "id", "college", "types", "is_open"
    )
    filter_horizontal = ("admin","buildings","grades")
@admin.register(Record)
class Record(admin.ModelAdmin):
    """任务管理"""
    list_display = (
        "id", "task","rule_str","grade_str","room_str","student_approved","worker","manager"
    )
    # filter_horizontal = ("admin","buildings","grades")