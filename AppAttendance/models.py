import json
from django.contrib.auth import get_user_model
import django.utils.timezone as timezone
from AppInformation.models import *
from cool.admin import admin_register
from cool.model import BaseModel
from django.conf import settings
from django.db import models


@admin_register
class Rule(models.Model):
    name = models.CharField(
        max_length=30, verbose_name=u'一级规则名称', null=True, blank=True)
    message = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=u'描述')
    codename = models.CharField(max_length=8, verbose_name=u'规则代码')
    is_person = models.BooleanField(verbose_name=u'是否个人有效')

    class Meta:
        verbose_name = '一级规则'
        verbose_name_plural = '一级规则'
        db_table = 'rule'

    def __str__(self):
        return self.name


@admin_register
class RuleDetails(models.Model):
    """二级规则"""
    name = models.CharField(max_length=20, verbose_name=u'二级规则名称')
    score = models.FloatField(verbose_name=u'分值', null=True, blank=True)
    rule = models.ForeignKey(
        'Rule', on_delete=models.CASCADE, verbose_name=u'一级分类')
    parent_id = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=u'父类')

    class Meta:
        db_table = 'rule_details'
        verbose_name = '二级规则'
        verbose_name_plural = '二级规则'

    def __str__(self):
        return self.name


class Task(BaseModel):
    """考勤任务管理"""
    GENDER_CHOICES1 = (
        (u'0', u'查寝'),
        (u'1', u'查卫生'),
        (u'2', u'晚自修'),
        (u'3', u'签到'),
    )
    COLLEGE_CHOICE = (
        (u'ZHJT', u'智慧交通'),
    )
    # GENDER_CHOICES1的修改需要注意BatchAttendance类的修改

    is_open = models.BooleanField(verbose_name='是否开启', default=False)
    types = models.CharField(
        max_length=20, choices=GENDER_CHOICES1, verbose_name=u'任务类型')
    roster = models.TextField(
        verbose_name=u'班表', null=True, blank=True, default=u'[]')

    college = models.CharField(max_length=10, choices=COLLEGE_CHOICE, verbose_name=u'分院编号')

    admin = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='admin', verbose_name=u'管理员')
    player = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='player', verbose_name=u'工作人员')
    grades = models.ManyToManyField(Grade, verbose_name=u'关联班级')

    buildings = models.TextField(null=True, blank=True, default=u'[]', verbose_name=u'关联房间')

    def get_grades(self):
        return self.grades.all().values_list('id', flat=True)

    def get_buildings(self):
        return json.loads(self.buildings)

    def get_admin(self):
        return json.loads(self.admin)

    def get_name(self):
        if self.college is not None:
            return self.college + " " + self.get_types_display()
        else:
            return self.get_types_display()

    def __str__(self):
        return self.get_name()

    class Meta:
        db_table = 'task'
        verbose_name = '任务'
        verbose_name_plural = '任务'


class Record(models.Model):
    """考勤记录"""
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="任务")
    rule = models.ForeignKey("RuleDetails",
                             on_delete=models.SET_NULL,
                             verbose_name="原因规则",
                             null=True,
                             blank=True
                             )

    rule_str = models.CharField(
        max_length=150, verbose_name="原因", null=True, blank=True)
    score = models.FloatField(null=True, blank=True, verbose_name="分值")

    room_str = models.CharField(
        max_length=20, verbose_name="寝室", null=True, blank=True)
    grade_str = models.CharField(
        max_length=20, verbose_name="班级", null=True, blank=True)

    worker_username = models.CharField(
        max_length=20, verbose_name="执行者学号", null=True, blank=True)
    worker_name = models.CharField(
        max_length=10, verbose_name="执行者姓名", null=True, blank=True)

    student_approved_username = models.CharField(
        max_length=20, verbose_name="被执行者学号", null=True, blank=True)
    student_approved_name = models.CharField(
        max_length=10, verbose_name="被执行者姓名", null=True, blank=True)

    manager_username = models.CharField(
        max_length=20, verbose_name="销假人学号", null=True, blank=True)
    manager_name = models.CharField(
        max_length=10, verbose_name="销假人姓名", null=True, blank=True)

    # 确保在save或者update的时候手动更新最后修改时间 因为某些批量操作不会触发
    star_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建日期')
    last_time = models.DateTimeField(auto_now=True, verbose_name=u'最后修改日期')

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     if self.student_approved:
    #         self.student_approved_username = self.student_approved.username
    #         self.student_approved_name = self.student_approved.name
    #     if self.manager:
    #         self.manager_username = self.manager.username
    #         self.manager_name = self.manager.name

    #     # 执行 save(), 将数据保存进数据库
    #     super().save(
    #         force_insert=force_insert,
    #         force_update=force_update,
    #         using=using,
    #         update_fields=update_fields
    #     )
    class Meta:
        db_table = 'record'
        verbose_name = '任务-考勤记录'
        verbose_name_plural = '任务-考勤记录'

    def __str__(self):
        """查寝记录: """
        return "考勤记录: " + str(self.id)
