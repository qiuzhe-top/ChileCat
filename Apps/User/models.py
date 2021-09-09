'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-09 19:01:22
Description: 
'''

from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from Apps.SchoolInformation.models import *
from cool.admin import admin_register

# 第三方账户绑定
class Token(models.Model):
    """
    Token
    """

    token = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")

    def __str__(self):
        return self.user.username + "的token:" + self.token

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户token'
        verbose_name_plural = '用户token'


# @admin_register
# class UserInfo(models.Model):
#     """
#     用户信息
#     """

#     name = models.CharField(max_length=20, verbose_name="姓名")
#     tel = models.CharField(max_length=20, verbose_name="电话", blank=True, null=True)
#     gender = models.CharField(
#         max_length=20,
#         verbose_name="性别",
#         choices=(("male", "男"), ("female", "女")),
#         null=True,
#         blank=True,
#     )
#     # 头像 https://a.jgp
#     photo = models.CharField(
#         max_length=2048, verbose_name="学生照片", null=True, blank=True
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户id")

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = ''
#         managed = True
#         verbose_name = '用户信息'
#         verbose_name_plural = '用户信息'


# class StudentInfo(models.Model):
#     """
#     学生信息
#     """

#     grade = models.ForeignKey(
#         Grade,
#         on_delete=models.CASCADE,
#         verbose_name="班级id",
#     )
#     user = models.OneToOneField(User, verbose_name="用户", on_delete=models.CASCADE)
#     photo = models.CharField(
#         max_length=2048, verbose_name="学生照片", null=True, blank=True
#     )

#     def __str__(self):
#         return self.user.username

#     class Meta:
#         db_table = ''
#         managed = True
#         verbose_name = '学生信息'
#         verbose_name_plural = '学生信息'


# class TeacherInfo(models.Model):
#     """
#     老师额外信息
#     """

#     teacher_extra_info = models.CharField(verbose_name="老师额外信息", max_length=50)
#     user = models.OneToOneField(User, verbose_name="用户", on_delete=models.CASCADE)

#     class Meta:
#         db_table = ''
#         managed = True
#         verbose_name = '老师信息'
#         verbose_name_plural = '老师信息'


# class TeacherForGrade(models.Model):
#     """
#     教师对应的班级
#     """

#     grade = models.OneToOneField(
#         Grade,
#         on_delete=models.CASCADE,
#         verbose_name="班级号",
#         related_name="related_to_teacher",
#     )
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="管理者账号",
#         related_name="related_to_grade",
#     )

#     class Meta:
#         verbose_name = "教师班级关系"
#         verbose_name_plural = "教师班级关系"

#     def __str__(self):
#         return self.user.name + "->" + self.grade.name
