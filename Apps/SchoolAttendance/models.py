from django.db import models
from django.contrib.auth.models import User
import datetime
from Apps.SchoolInformation.models import *
from cool.admin import admin_register
from cool.model import BaseModel

# Create your models here.


@admin_register
class Rule(models.Model):
    name = models.CharField(
        max_length=30, verbose_name=u'名称', null=True, blank=True)
    message = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=u'描述')
    codename = models.CharField(max_length=8, verbose_name=u'规则代码')
    is_person = models.BooleanField(verbose_name=u'是否个人有效')
    class Meta:

        verbose_name = '一级规则'
        verbose_name_plural = '一级规则'

    def __str__(self):
        return self.name

@admin_register
class RuleDetails(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'名称')
    score = models.IntegerField(verbose_name=u'分值', null=True, blank=True)
    rule = models.ForeignKey(
        'Rule', on_delete=models.CASCADE, verbose_name=u'一级分类')
    parent_id = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=u'父类')

    class Meta:

        verbose_name = '二级规则'
        verbose_name_plural = '二级规则'

    def __str__(self):
        return self.name


@admin_register(
    list_display=['college', 'types','is_open']
    # change_view_readonly_fields=['college','types'],
)
class Task(BaseModel):
    """考勤任务管理"""
    GENDER_CHOICES1 = (
        (u'0', u'查寝'),
        (u'1', u'查卫生'),
        (u'2', u'晚自修')
    )
    is_open = models.BooleanField(verbose_name='是否开启',default=False)
    types = models.CharField(
        max_length=20, choices=GENDER_CHOICES1, verbose_name=u'任务类型')
    roster = models.TextField(
        verbose_name=u'班表', null=True, blank=True, default=u'[]')
    college = models.ForeignKey(
        College, null=True, blank=True, on_delete=models.CASCADE, verbose_name=u'分院')
    admin = models.ManyToManyField(
        User, null=True, blank=True,  verbose_name=u'管理员')
    buildings = models.ManyToManyField(
        Building, null=True, blank=True, verbose_name=u'关联楼')
    grades = models.ManyToManyField(
        Grade, null=True, blank=True, verbose_name=u'关联班级')

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务'
        permissions  = (
            ('undo_record_admin', "管理员销假"),
        )
    def get_name(self):
        if self.college != None:
            return self.college.name + " " + self.get_types_display()
        else:
            return self.get_types_display()

    def __str__(self):
        """Unicode representation of Manage."""
        return  self.get_name()

@admin_register
class Record(models.Model):
    """考勤记录"""
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="任务")
    rule_str = models.CharField(
        max_length=150, verbose_name="原因", null=True, blank=True)
    score = models.IntegerField(null=True, blank=True, verbose_name="分值") 
    rule = models.ForeignKey("RuleDetails",
                                on_delete=models.SET_NULL,
                                verbose_name="原因规则",
                                null=True,
                                blank=True
                             )

    room_str = models.CharField(
        max_length=20, verbose_name="寝室", null=True, blank=True)
    grade_str = models.CharField(
        max_length=20, verbose_name="班级", null=True, blank=True)

    student_approved = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="被执行者", related_name="stu_approved",
    )

    worker = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="执行者", related_name="task_worker",
    )

    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="销假人",
        related_name="销假人",
    )
     
    # 确保在save或者update的时候手动更新最后修改时间 因为某些批量操作不会触发
    star_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u'创建日期')
    last_time = models.DateTimeField(auto_now=True, verbose_name=u'最后修改日期')

    class Meta:
        verbose_name = '任务-考勤记录'
        verbose_name_plural = '任务-考勤记录'

    def __str__(self):
        """查寝记录: """
        return "考勤记录: " + str(self.id)

@admin_register(
    raw_id_fields = ['user',]
)
class TaskPlayer(models.Model):
    '''任务-参与者
    '''
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name=u'任务')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    is_finish = models.BooleanField(verbose_name="是否完成", default=False)
    star_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建日期')
    last_time = models.DateTimeField(auto_now=True, verbose_name=u'最后修改日期')

    class Meta:
        verbose_name = '任务-参与者'
        verbose_name_plural = '任务-参与者'



# TODO 后面3张表 考虑采用内存作为载体
@admin_register
class RoomHistory(models.Model):
    """考勤-房间
    记录房间是否被检查的状态，记录这个房间是否被点名和查卫生执行过
    """
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, verbose_name="房间号", related_name="room_history"
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name=u'任务')
    is_knowing = models.BooleanField(verbose_name='是否查寝',null=True,blank=True)
    is_health = models.BooleanField(verbose_name='是否查卫生',null=True,blank=True)

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '寝室被查记录'
        verbose_name_plural = '寝室被查记录'

    def __str__(self):
        return self.room.floor.building.name + self.room.floor.name + self.room.name

@admin_register
class TaskFloorStudent(models.Model):
    '''考勤-房间-学生
    记录房间里面的学生检查状态 是   缺寝 还是 在寝
    '''
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name=u'任务')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=u'用户')
    flg = models.BooleanField(verbose_name='是否在寝室',default=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = '学生在寝情况'

@admin_register
class UserCall(models.Model):
    '''点名-学生
    当学生在点名的时候被记录就变动点名类型
    '''
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name=u'任务')
        
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=u'用户', related_name="user_call")

    flg = models.BooleanField(verbose_name='是否在班',default=None,null=True,blank=True)

    rule = models.ForeignKey("RuleDetails", on_delete=models.CASCADE,
                             verbose_name="第几次点名", null=True, blank=True)
    class Meta:
        verbose_name_plural = '学生点名情况'
