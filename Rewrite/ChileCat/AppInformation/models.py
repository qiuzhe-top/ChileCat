'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 16:16:36
Description: 
'''
from atexit import register
from Core.common.models import ActiveBase
from cool.admin import admin_register
from django.conf import settings
from django.db import models

# Create your models here.

@admin_register
class Grade(models.Model):
    """
    学校班级
    """
    id = models.CharField(primary_key=True ,max_length=20, verbose_name="班级号")
    college = models.ForeignKey(
        "College",null=True, blank=True, related_name="college_grades", on_delete=models.CASCADE, verbose_name="学院")

    class Meta:
        verbose_name = "学校班级"
        verbose_name_plural = "学校班级"

@admin_register
class College(models.Model):
    """
    学校分院
    """
    name = models.CharField(max_length=50, verbose_name="学院名称")
    code_name = models.CharField(max_length=50, verbose_name="代码")

    class Meta:
        verbose_name = "学校分院"
        verbose_name_plural = "学校分院"

    def __str__(self):
        return self.name

@admin_register
class DormitoryBuilding(models.Model):
    id = models.CharField(max_length=6,primary_key=True,default='#')

    def get_name(self):
        return self.id

    def __str__(self) -> str:
        return self.get_name()
    class Meta:
        verbose_name = '宿舍信息'
        verbose_name_plural = verbose_name
        db_table = 'dormitory_building'

@admin_register
class StuInRoom(ActiveBase):
    """宿舍入住信息"""
    
    room = models.ForeignKey(
        'DormitoryBuilding', on_delete=models.CASCADE, verbose_name="房间id", related_name="stu_in_room"
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="用户")

    bed_position = models.IntegerField(blank=True, null=True, verbose_name="床铺位置")


    def get_room(self):
        return self.room.get_name()

    def __str__(self):
        """返回房间号"""
        return self.get_room()
    class Meta:
        verbose_name = '宿舍入住信息'
        verbose_name_plural = '宿舍入住信息'
        permissions = [
            ('operate-stu_in_room_view', "operate-查询学生位置权限")
        ]

