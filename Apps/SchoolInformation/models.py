from django.db import models
from django.contrib.auth.models import User

# Create your models here.


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


class Grade(models.Model):
    """
    班级
    """
    name = models.CharField(max_length=20, verbose_name="班级号", unique=True)
    college = models.ForeignKey(
        "College",null=True, blank=True, related_name="grade", on_delete=models.CASCADE, verbose_name="学院")
    whole_grade = models.ForeignKey(
        "WholeGrade", on_delete=models.CASCADE, related_name="grade", verbose_name="年级",
        null=True, blank=True
    )

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = "班级"

    def get_users(self):
        '''获取班级内学生'''
        user_list = self.student_grade.all().values_list('user',flat=True)
        return User.objects.filter(id__in=list(user_list))

    def __str__(self):
        return self.name


class WholeGrade(models.Model):
    """年级"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tea_for_whole_grade", null=True, blank=True, verbose_name="辅导员账号"
    )
    name = models.CharField(max_length=20, verbose_name="年级")

    class Meta:
        verbose_name = "年级"
        verbose_name_plural = "年级"

    def __str__(self):
        return self.name


class College(models.Model):
    """
    分院
    """
    name = models.CharField(max_length=50, verbose_name="学院名称")
    code_name = models.CharField(max_length=50, verbose_name="代码")

    class Meta:
        verbose_name = "分院"
        verbose_name_plural = "分院"

    def __str__(self):
        return self.name


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
    health_status = models.BooleanField(verbose_name="卫生检查状态", default=False)
    dorm_status = models.BooleanField(verbose_name="晚查寝状态", default=False)

    class Meta:
        """Meta definition for Room."""

        verbose_name = '房间'
        verbose_name_plural = '房间'
        permissions = [
            ('operate-room_view', "operate-查询宿舍楼房间权限")
        ]
    def get_room(self):
        return self.floor.building.name + "#" + self.floor.name + self.name
        
    def __str__(self):
        """返回房间号"""
        return self.floor.building.name + self.floor.name + self.name


class StuInRoom(models.Model):
    """房间里有哪些学生."""
    room = models.ForeignKey(
        'Room', on_delete=models.CASCADE, verbose_name="房间id", related_name="stu_in_room"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, verbose_name="学生"
    )
    bed_position = models.CharField(
        max_length=150, verbose_name="床铺位置", default="1")

    class Meta:
        verbose_name = '寝室信息'
        verbose_name_plural = '寝室信息'
        permissions = [
            ('operate-stu_in_room_view', "operate-查询学生位置权限")
        ]

    def get_room(self):
        return self.room.floor.building.name + self.room.floor.name + self.room.name

    def __str__(self):
        """返回房间号"""
        return self.get_room()