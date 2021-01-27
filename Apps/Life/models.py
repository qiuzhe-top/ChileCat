'''
Life数据库模型
'''
from django.db import models
import Apps.User
# Create your models here.
class Building(models.Model):
    """楼"""
    budnum = models.CharField(max_length = 50,verbose_name="楼号")
    class Meta:
        """Meta definition for building."""
        verbose_name = '宿舍楼'
        verbose_name_plural = '宿舍楼'
    def __str__(self):
        """Unicode representation of building."""
        return self.budnum

class Floor(models.Model):
    """楼层."""
    budid = models.ForeignKey(
        'Building', on_delete=models.CASCADE,
        related_name="floor",verbose_name="楼号"
        )
    floornum = models.CharField(max_length = 20,verbose_name="楼层号")

    class Meta:
        """Meta definition for floor."""
        verbose_name = '楼层'
        verbose_name_plural = '楼层'

    def __str__(self):
        """Unicode representation of floor."""
        return self.budid.budnum + '-' + self.floornum

class Room(models.Model):
    """房间"""
    roomnum = models.CharField(max_length = 20,verbose_name="房间号")
    floor = models.ForeignKey(
        'Floor', on_delete=models.CASCADE,verbose_name="层",related_name="room"
        )
    status = models.CharField(max_length = 20,verbose_name="状态",default="0")

    class Meta:
        """Meta definition for Room."""

        verbose_name = '房间'
        verbose_name_plural = '房间'

    def __str__(self):
        """返回房间号"""
        return self.floor.budid.budnum + self.floor.floornum + self.roomnum

class StuInRoom(models.Model):
    """房间里有哪些学生."""
    roomid = models.ForeignKey(
        'Room', on_delete=models.CASCADE,verbose_name="房间id",related_name="stuinroom"
        )
    stuid = models.ForeignKey(
        'User.User',
         on_delete=models.CASCADE,verbose_name="学生",related_name="stuinroom"
        )
    bedposition = models.CharField(max_length = 150,verbose_name="床铺位置",default="1")
    '''由于前端奇怪的要求,这里0是在寝室,1是不在寝室'''
    status = models.CharField(max_length = 50,verbose_name="是否在寝",default="0")

    class Meta:
        verbose_name = '寝室信息'
        verbose_name_plural = '寝室信息'

    def __str__(self):
        """返回房间号"""
        return self.roomid.floor.budid.budnum + self.roomid.floor.floornum + self.roomid.roomnum

class RoomHistory(models.Model):
    """寝室被查记录"""
    roomid = models.ForeignKey(
        Room, on_delete=models.CASCADE,verbose_name="房间号",related_name="roomhistory"
        )
    managerid = models.ForeignKey(
        'User.User', on_delete=models.CASCADE,verbose_name="查寝人",related_name="roomhistory"
        )
    createdtime = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name="创建时间")


    class Meta:
        """Meta definition for RoomHistory."""
        verbose_name = '寝室被查记录'
        verbose_name_plural = '寝室被查记录'

    def __str__(self):
        """Unicode representation of RoomHistory."""
        return self.roomid.floor.budid.budnum + self.roomid.floor.floornum + self.roomid.roomnum

class TaskRecord(models.Model):
    """任务记录(指被查到不在寝室的)"""
    workerid = models.ForeignKey(
        'User.User', on_delete=models.CASCADE,
        verbose_name="执行者",related_name="taskworker"
        )
    objstuid = models.ForeignKey(
        'User.User', on_delete=models.CASCADE,
        verbose_name="被执行者",related_name="taskedstu"
        )
    reason = models.CharField(max_length = 50,verbose_name="原因")
    flag = models.CharField(max_length = 20,verbose_name="是否归寝")
    createdtime = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name="创建时间")
    lastmodifytime = models.DateTimeField(auto_now=False, auto_now_add=False,verbose_name="最后修改时间")
    buildingid = models.ForeignKey(
        'Building', on_delete=models.CASCADE,
        verbose_name="楼id",related_name="taskbuilding"
        )
    roomid = models.ForeignKey(
        'Room', on_delete=models.CASCADE,
        related_name="taskrecord",verbose_name="寝室号"
        )
    managerid = models.ForeignKey(
        'User.User', on_delete=models.CASCADE,
        blank=True,null=True,default="",
        verbose_name="销假人",
        related_name="销假人"
        )


    class Meta:
        """Meta definition for TaskRecord."""

        verbose_name = '查寝记录'
        verbose_name_plural = '查寝记录'

    def __str__(self):
        """查寝记录: XXX"""
        return "查寝记录: " +str(self.id)

class Manage(models.Model):
    """Model definition for Manage."""
    idcodetime = models.DateField(auto_now=False, auto_now_add=False,verbose_name="验证码生成时间")
    idcode = models.CharField(max_length = 50,verbose_name="验证码")
    console = models.CharField(max_length = 50,verbose_name="类型")
    class Meta:
        """Meta definition for Manage."""

        verbose_name = '管理列表'
        verbose_name_plural = '管理列表'

    def __str__(self):
        """Unicode representation of Manage."""
        return "验证码: " + self.idcode + "时间: " + self.idcodetime.strftime("%Y-%m-%d-%H")
