"""
Life数据库模型
"""
from django.db import models
from django.contrib.auth.models import User
from Apps.User.models import College, Grade


# Create your models here.
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


class Floor(models.Model):
    """楼层."""
    building = models.ForeignKey(
        'Building', on_delete=models.CASCADE,
        related_name="floor", verbose_name="楼号"
    )
    name = models.CharField(max_length=20, verbose_name="楼层号")

    class Meta:
        """Meta definition for floor."""
        verbose_name = '楼层'
        verbose_name_plural = '楼层'
        permissions = [
            ('operate-floor_view', "operate-查询宿舍楼层权限")
        ]

    def __str__(self):
        """Unicode representation of floor."""
        return self.building.name + '-' + self.name


class Room(models.Model):
    """房间"""
    name = models.CharField(max_length=20, verbose_name="房间号")
    floor = models.ForeignKey(
        'Floor', on_delete=models.CASCADE, verbose_name="层", related_name="room"
    )
    status = models.CharField(max_length=20, verbose_name="状态", default="0")

    class Meta:
        """Meta definition for Room."""

        verbose_name = '房间'
        verbose_name_plural = '房间'
        permissions = [
            ('operate-room_view', "operate-查询宿舍楼房间权限")
        ]

    def __str__(self):
        """返回房间号"""
        return self.floor.building.name + self.floor.name + self.name


class StuInRoom(models.Model):
    """房间里有哪些学生."""
    room = models.ForeignKey(
        'Room', on_delete=models.CASCADE, verbose_name="房间id", related_name="stu_in_room"
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE, verbose_name="学生", related_name="stu_in_room"
    )
    bed_position = models.CharField(max_length=150, verbose_name="床铺位置", default="1")
    '''由于前端奇怪的要求,这里0是在寝室,1是不在寝室'''
    status = models.CharField(max_length=50, verbose_name="是否在寝", default="1")

    class Meta:
        verbose_name = '寝室信息'
        verbose_name_plural = '寝室信息'
        permissions = [
            ('operate-stu_in_room_view', "operate-查询学生位置权限")
        ]

    def __str__(self):
        """返回房间号"""
        return self.room.floor.building.name + self.room.floor.name + self.room.name


class RoomHistory(models.Model):
    """寝室被查记录"""
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, verbose_name="房间号", related_name="room_history"
    )
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="查寝人", related_name="room_approved"
    )
    created_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="创建时间")

    class Meta:
        """Meta definition for RoomHistory."""
        verbose_name = '寝室被查记录'
        verbose_name_plural = '寝室被查记录'
        permissions = [
            ('operate-room_history_view', "operate-查询查寝记录权限")
        ]

    def __str__(self):
        """Unicode representation of RoomHistory."""
        return self.room.floor.building.name + self.room.floor.name + self.room.name

