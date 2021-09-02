'''
Author: 邹洋
Date: 2021-09-02 14:36:25
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-02 14:47:22
Description: 
'''
from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(HomeWork)
class HomeWork(admin.ModelAdmin):
    """任务管理"""
    # list_display = '__all__'