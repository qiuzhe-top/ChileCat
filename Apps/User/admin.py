'''
admin.py
'''
from django.contrib import admin
from . import models
from django.utils.html import format_html


# @admin.register(models.User)
# class UserTeleAdmin(admin.ModelAdmin):
#     list_display = ("id","user_name","pass_word","django_user")
@admin.register(models.Token)
class TokenTeleAdmin(admin.ModelAdmin):
    list_display = ("id", "token", "user")


@admin.register(models.UserInfo)
class UserInfoTeleAdmin(admin.ModelAdmin):
    # def user_to_role(self,obj):
    #     roles_count = obj.user_role.count()
    #     if roles_count > 0:
    #         return "该用户有"+str(roles_count)+"个角色"
    #     return format_html('<span style="color:#8E8E8E;">(该用户无角色)</span>')
    # def show_tel(self,obj):
    #     if obj.tel:
    #         return obj.tel
    #     return format_html('<span style="color:#8E8E8E;">(无电话信息)</span>')
    list_display = ("id", "user_id", "name", "tel", "identity")  # ,"user_to_role"
    # user_to_role.short_description = "用户角色"
    # filter_horizontal = ['user_role']
    empty_value_display = format_html('<span style="color:#8E8E8E;">(内容为空)</span>')


@admin.register(models.StudentInfo)
class StudentInfoTeleAdmin(admin.ModelAdmin):
    list_display = ("id", "grade_id", "user_id", "students_photo", "parents_call")


@admin.register(models.TeacherInfo)
class TeacherInfoTeleAdmin(admin.ModelAdmin):
    list_display = ("id", "teacher_extra_info", "user_id")


@admin.register(models.TeacherForGrade)
class TeacherForGradeTeleAdmin(admin.ModelAdmin):
    list_display = ("id", "grade_id", "user_id")


@admin.register(models.TeacherForCollege)
class TeacherForCollegeTeleAdmin(admin.ModelAdmin):
    list_display = ("college_id", "user_id")


@admin.register(models.Grade)
class GradeTeleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "college_id", "whole_grade")


@admin.register(models.College)
class CollegeTeleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Tpost)
class TpostTeleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(models.WholeGrade)
class WholeGradeTeleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'name')


@admin.register(models.UserMood)
class UserMoodTeleAdmin(admin.ModelAdmin):
    list_display = ('id', 'mod_level', 'message', 'user', 'Grade', 'riqi')
    search_fields = ('user', 'Grade', 'mod_level')  # 添加快速查询栏

    def func(self, request, queryset):
        # queryset.update(created_time='2018-09-28')
        print(6666666666)
        # 批量更新我们的created_time字段的值为2018-09-28

    func.short_description = "中文显示自定义Actions"
    actions = [func, ]
