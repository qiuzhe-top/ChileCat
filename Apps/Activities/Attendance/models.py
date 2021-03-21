# from django.db import models
# from django.utils import timezone
# from Apps.User.models import *
#
#
# # Create your models here.
# class PunishmentSort(models.Model):
#     name = models.CharField(max_length=30, verbose_name=u'名称', null=True, blank=True)
#     codename = models.CharField(max_length=30, verbose_name=u'代码名称')
#     message = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'描述')
#
#     class Meta:
#         """Meta definition for TaskRecord."""
#
#         verbose_name = '规则一级分类'
#         verbose_name_plural = '规则一级分类'
#
#     def __str__(self):
#         return self.name
#
#
# class Punishment(models.Model):
#     """扣分分类"""
#     name = models.CharField(max_length=20, verbose_name=u'名称')
#     sort = models.ForeignKey('PunishmentSort', on_delete=models.CASCADE, verbose_name=u'所属分类')
#
#     class Meta:
#         """Meta definition for TaskRecord."""
#
#         verbose_name = '规则二级分类'
#         verbose_name_plural = '规则二级分类'
#
#     def __str__(self):
#         return self.name
#
#
# class PunishmentDetails(models.Model):
#     name = models.CharField(max_length=20, verbose_name=u'名称')
#     score = models.IntegerField(verbose_name=u'分值', null=True, blank=True)
#     is_person = models.BooleanField(verbose_name=u'是否个人有效')
#     punishment = models.ForeignKey('Punishment', on_delete=models.CASCADE, verbose_name=u'扣分类型')
#
#     class Meta:
#         """Meta definition for TaskRecord."""
#
#         verbose_name = '扣分详情'
#         verbose_name_plural = '扣分详情'
#
#     def __str__(self):
#         return self.name
#
#
# class TaskRecord(models.Model):
#     """公共任务记录信息"""
#     task_type = models.ForeignKey('Manage', on_delete=models.CASCADE, verbose_name="任务类型")
#     worker = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         verbose_name="执行者", related_name="task_worker",
#         null=True,
#         blank=True
#     )
#     student_approved = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         verbose_name="被执行者", related_name="stu_approved",
#         null=True,
#         blank=True
#     )
#     manager = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         blank=True, null=True, default="",
#         verbose_name="销假人",
#         related_name="销假人",
#     )
#     score = models.CharField(max_length=10, null=True, blank=True, verbose_name="分值")
#     reason = models.ForeignKey("PunishmentDetails",
#                                on_delete=models.CASCADE,
#                                related_name="task",
#                                verbose_name="原因",
#                                null=True,
#                                blank=True
#                                )
#     reason_str = models.CharField(max_length=150, verbose_name="原因", null=True, blank=True)
#     created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
#     # 确保在save或者update的时候手动更新最后修改时间
#     last_modify_time = models.DateTimeField(verbose_name="最后修改时间", default=timezone.now)
#     room_str = models.CharField(max_length=20, verbose_name="寝室", null=True, blank=True)
#     grade_str = models.CharField(max_length=20, verbose_name="班级", null=True, blank=True)
#
#     # 如果以后新建活动，请在此添加新的字段,注意一定要把null和blank为true
#
#     class Meta:
#         """Meta definition for TaskRecord."""
#
#         verbose_name = '考勤记录'
#         verbose_name_plural = '考勤记录'
#         permissions = [
#             ('operate-task_record_add', "operate-考勤记录添加权限"),
#             ('operate-task_record_cancel', "operate-销假权限")
#         ]
#
#     def __str__(self):
#         """查寝记录: XXX"""
#         return "考勤记录: " + str(self.id)
#
#
# class Manage(models.Model):
#     """考勤任务管理"""
#     GENDER_CHOICES = (
#         (u'dorm', u'查寝'),
#         (u'health', u'查卫生'),
#         (u'evening_study', u'晚自修'),
#     )
#
#     types = models.CharField(max_length=20, choices=GENDER_CHOICES, verbose_name=u'任务类型')
#     console_code = models.CharField(max_length=2, verbose_name="是否开启", default="0")
#     college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name=u'分院')
#     verification_code = models.CharField(max_length=50, verbose_name="验证码", default="00000000")
#     generate_time = models.DateField(auto_now=False, auto_now_add=False, verbose_name="验证码生成时间")
#
#     class Meta:
#         """Meta definition for Manage."""
#
#         verbose_name = '管理列表'
#         verbose_name_plural = '管理列表'
#         permissions = [
#             ('operate-verification_code_flash', "operate-刷新验证码权限"),
#             ('operate-verification_code_generate', "operate-生成验证码权限"),
#             ('operate-verification_code_view', "operate-查看验证码权限")
#         ]
#
#     def __str__(self):
#         """Unicode representation of Manage."""
#         return self.types
