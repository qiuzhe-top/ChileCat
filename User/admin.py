'''
admin.py
'''
from django.contrib import admin
from .models import User,Token,Tpost,UserInfo,StudentInfo,TeacherInfo,TeacherForGrade,Grade,College,Permission,UserForPermission,TeacherForCollege

@admin.register(User)
class UserTeleAdmin(admin.ModelAdmin):
    list_display = ("id","user_name","pass_word")
@admin.register(Token)
class TokenTeleAdmin(admin.ModelAdmin):
    list_display = ("id","token")
@admin.register(UserInfo)
class UserInfoTeleAdmin(admin.ModelAdmin):
    list_display = ("id","user_id","name","tel","identity")
@admin.register(StudentInfo)
class StudentInfoTeleAdmin(admin.ModelAdmin):
    list_display = ("id","student_id","grade_id","user_id")
@admin.register(TeacherInfo)
class TeacherInfoTeleAdmin(admin.ModelAdmin):
    list_display = ("id","teacher_extra_info","user_id")
@admin.register(TeacherForGrade)
class TeacherForGradeTeleAdmin(admin.ModelAdmin):
    list_display = ("id","grade_id","user_id")
@admin.register(TeacherForCollege)
class TeacherForCollegeTeleAdmin(admin.ModelAdmin):
    list_display = ("college_id","user_id")
@admin.register(Grade)
class GradeTeleAdmin(admin.ModelAdmin):
    list_display = ("id","name","college_id")
@admin.register(College)
class CollegeTeleAdmin(admin.ModelAdmin):
    list_display = ("id","name")
@admin.register(Permission)
class PermissionTeleAdmin(admin.ModelAdmin):
    list_display = ("id","name","message")
@admin.register(UserForPermission)
class UserForPermissionTeleAdmin(admin.ModelAdmin):
    list_display = ("id","user_id","perm_id")
@admin.register(Tpost)
class TpostTeleAdmin(admin.ModelAdmin):
    list_display = ('id','user')
