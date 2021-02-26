"""
数据库模型
"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ASK_TYPE = (
    ("draft", "草稿"),
    ("first_audit", "班主任审核"),
    ("second_audit", "辅导员审核"),
    ("college_audit", "院级审核"),
    ("university_audit", "校级审核"),
    ("passed", "通过"),
    ("failed", "不通过")
)


class Ask(models.Model):
    """
    请假条
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="用户id", related_name="user")
    status = models.CharField(max_length=20, choices=ASK_TYPE, verbose_name="审核状态", default="draft")
    contact_info = models.CharField(max_length=20, verbose_name="联系信息", null=True, blank=True)
    parents_call = models.CharField(max_length=20, verbose_name="家长联系信息", null=True, blank=True)
    ask_type = models.ForeignKey(
        "AskType", on_delete=models.CASCADE, verbose_name="请假类别", null=True, blank=True
    )
    reason = models.CharField(max_length=200, verbose_name="理由")
    place = models.CharField(max_length=50, verbose_name="地点")
    ask_state = models.CharField(max_length=50, verbose_name="是否完成", choices=(
        ("1", "完成"),
        ("0", "未完成")
    ), default="0")
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="开始时间")
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="结束时间")
    extra_end_time = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="续假时间")
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")
    grade = models.ForeignKey(
        'User.Grade', null=True, blank=True,
        on_delete=models.SET_NULL, verbose_name=u'班级')
    '''
        目前设计为一个班级固定对应一个老师
    '''
    approve_user = models.ForeignKey(
        User,
        verbose_name="审批老师的id",
        on_delete=models.CASCADE,
        related_name="pass_id", default=1, blank=True, null=True)

    def __str__(self):
        return "请假条id: " + str(self.id)

    class Meta:
        verbose_name = "请假条"
        verbose_name_plural = "请假条"
        permissions = [
            ('operate-ask_view', "operate-普通查看请假条权限"),
            ('operate-ask_monitor_view', "operate-班委查看请假条权限"),
            ('operate-ask_teacher_view', "operate-老师查看请假条权限"),
        ]


class Audit(models.Model):
    """
    审批记录
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户id")
    approve_teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="审批人id", related_name="audit_teacher"
    )
    ask = models.ForeignKey(
        "Ask", null=True, blank=True,
        on_delete=models.SET_NULL, verbose_name="请假单id")
    status = models.CharField(max_length=20, choices=ASK_TYPE, verbose_name="操作后状态")
    explain = models.CharField(max_length=20, verbose_name="审核说明")
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="修改时间")

    def __str__(self):
        return "审批记录" + str(self.id)

    class Meta:
        ordering = ['-created_time']
        verbose_name = "审核情况表"
        verbose_name_plural = "审核情况表"
        permissions = [
            ('operate-audit_class_teacher', "operate-班主任审批请假条权限"),
            ('operate-audit_grade_teacher', "operate-辅导员审批请假条权限"),
            ('operate-audit_college_teacher', "operate-院领导审核假条权限"),
            ('operate-audit_school_teacher', "operate-校长审核假条权限")
        ]


class AskType(models.Model):
    """请假类别."""

    type_name = models.CharField(max_length=150, verbose_name="请假类别")

    class Meta:
        """Meta definition for AskType."""

        verbose_name = '请假类别'
        verbose_name_plural = '请假类别表'
        permissions = [
            ('operate-ask_type_view', "operate-查看请假类别权限")
        ]

    def __str__(self):
        """Unicode representation of AskType."""
        return self.type_name
