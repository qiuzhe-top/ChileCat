'''
admin.py
'''
from django.contrib import admin
from . import models

@admin.register(models.User)
class UserTeleAdmin(admin.ModelAdmin):
    list_display = ("id","user_name","pass_word")
@admin.register(models.Token)
class TokenTeleAdmin(admin.ModelAdmin):
    list_display = ("id","token")
@admin.register(models.UserInfo)
class UserInfoTeleAdmin(admin.ModelAdmin):
    list_display = ("id","user_id","name","tel","identity")
@admin.register(models.StudentInfo)
class StudentInfoTeleAdmin(admin.ModelAdmin):
    list_display = ("id","grade_id","user_id")
@admin.register(models.TeacherInfo)
class TeacherInfoTeleAdmin(admin.ModelAdmin):
    list_display = ("id","teacher_extra_info","user_id")
@admin.register(models.TeacherForGrade)
class TeacherForGradeTeleAdmin(admin.ModelAdmin):
    list_display = ("id","grade_id","user_id")
@admin.register(models.TeacherForCollege)
class TeacherForCollegeTeleAdmin(admin.ModelAdmin):
    list_display = ("college_id","user_id")
@admin.register(models.Grade)
class GradeTeleAdmin(admin.ModelAdmin):
    list_display = ("id","name","college_id")
@admin.register(models.College)
class CollegeTeleAdmin(admin.ModelAdmin):
    list_display = ("id","name")
@admin.register(models.Permission)
class PermissionTeleAdmin(admin.ModelAdmin):
    list_display = ("id","name","message")
@admin.register(models.UserForPermission)
class UserForPermissionTeleAdmin(admin.ModelAdmin):
    list_display = ("id","user_id","perm_id")
@admin.register(models.Tpost)
class TpostTeleAdmin(admin.ModelAdmin):
    list_display = ('id','user')


@admin.register(models.UserMood)
class UserMoodTeleAdmin(admin.ModelAdmin):
    list_display = ('id','mod_level','message','user','Grade','riqi')
    search_fields = ('user','Grade','mod_level') # 添加快速查询栏

    def func(self, request, queryset):
        # queryset.update(created_time='2018-09-28')
        print(6666666666)
        #批量更新我们的created_time字段的值为2018-09-28
            
    func.short_description = "中文显示自定义Actions"
    actions = [func, ]