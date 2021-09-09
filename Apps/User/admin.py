'''
Author: 邹洋
Date: 2021-09-08 19:34:17
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-09 06:59:31
Description: 
'''
from Apps.User.models import StudentInfo
from django.contrib import admin



# @admin.register(StudentInfo)
# class StudentInfoAdmin(admin.ModelAdmin):
#     list_display = ('id','user__username')