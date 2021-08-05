'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-04 20:51:22
Description: 
'''
from django.db import models
from django.contrib.auth.models import User
from cool.admin import admin_register
from django.utils import tree

# Create your models here.

@admin_register
class TeacherForCollege(models.Model):
    """
    领导对应的分院
    """
    college = models.ForeignKey(
        "College", on_delete=models.CASCADE, verbose_name="分院号")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="管理者账号")

    class Meta:
        verbose_name = "老师院级关系"
        verbose_name_plural = "教师院级关系"

@admin_register
class Grade(models.Model):
    """
    学校班级
    """
    name = models.CharField(max_length=20, verbose_name="班级号", unique=True)
    college = models.ForeignKey(
        "College",null=True, blank=True, related_name="grade", on_delete=models.CASCADE, verbose_name="学院")
    whole_grade = models.ForeignKey(
        "WholeGrade", on_delete=models.CASCADE, related_name="grade", verbose_name="年级",
        null=True, blank=True
    )

    class Meta:
        verbose_name = "学校班级"
        verbose_name_plural = "学校班级"

    def get_users(self):
        '''获取班级内学生'''
        user_list = self.studentinfo_set.all().values_list('user',flat=True)
        return User.objects.filter(id__in=list(user_list))

    def __str__(self):
        return self.name

@admin_register
class WholeGrade(models.Model):
    """学校年级"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tea_for_whole_grade", null=True, blank=True, verbose_name="辅导员账号"
    )
    name = models.CharField(max_length=20, verbose_name="年级")

    class Meta:
        verbose_name = "学校年级"
        verbose_name_plural = "学校年级"

    def __str__(self):
        return self.name

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
class Building(models.Model):
    """楼"""
    name = models.CharField(max_length=50, verbose_name="楼号")

    class Meta:
        """Meta definition for building."""
        verbose_name = '宿舍楼'
        verbose_name_plural = '宿舍楼'
        permissions = [
            ('operate-building_view', "operate-查询宿舍楼权限")
        ]

    def __str__(self):
        """Unicode representation of building."""
        return self.name

@admin_register
class Floor(models.Model):
    """宿舍楼层."""
    building = models.ForeignKey(
        'Building', on_delete=models.CASCADE,
        related_name="floor", verbose_name="楼号"
    )
    name = models.CharField(max_length=20, verbose_name="楼层号")
    is_open = models.BooleanField(verbose_name="是否可用",default=True)
    class Meta:
        """Meta definition for floor."""
        verbose_name = '宿舍楼层'
        verbose_name_plural = '宿舍楼层'
        permissions = [
            ('operate-floor_view', "operate-查询宿舍楼层权限")
        ]

    def __str__(self):
        """Unicode representation of floor."""
        return self.building.name + '-' + self.name

@admin_register
class Room(models.Model):
    """宿舍房间信息"""
    name = models.CharField(max_length=20, verbose_name="房间号")
    floor = models.ForeignKey(
        'Floor', on_delete=models.CASCADE, verbose_name="层", related_name="room"
    )
    health_status = models.BooleanField(verbose_name="卫生检查状态",default=False)
    dorm_status = models.BooleanField(verbose_name="晚查寝状态",default=False)

    class Meta:
        """Meta definition for Room."""

        verbose_name = '宿舍房间信息'
        verbose_name_plural = '宿舍房间信息'
        permissions = [
            ('operate-room_view', "operate-查询宿舍楼房间权限")
        ]
    def get_room(self):
        return self.floor.building.name + "#" + self.floor.name + self.name
        
    def __str__(self):
        """返回房间号"""
        return self.floor.building.name + "#" + self.floor.name + self.name

@admin_register
class StuInRoom(models.Model):
    """宿舍入住信息"""
    room = models.ForeignKey(
        'Room', on_delete=models.CASCADE, verbose_name="房间id", related_name="stu_in_room"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, verbose_name="学生"
    )
    bed_position = models.IntegerField(
        verbose_name="床铺位置")

    class Meta:
        verbose_name = '宿舍入住信息'
        verbose_name_plural = '宿舍入住信息'
        permissions = [
            ('operate-stu_in_room_view', "operate-查询学生位置权限")
        ]

    def get_room(self):
        return self.room.floor.building.name + self.room.floor.name + self.room.name

    def __str__(self):
        """返回房间号"""
        return self.get_room()