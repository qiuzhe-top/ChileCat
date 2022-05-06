'''
Author: 邹洋
Date: 2022-02-07 11:06:28
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-04-30 16:47:27
Description: 
'''
from AppInformation.models import Grade
from cool.admin import admin_register
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from shortuuidfield import ShortUUIDField  # 使用shortuuid作为User表的主键，使数据更加的安全


@admin_register()
class Token(models.Model):
    """
    Token
    """

    token = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="用户")

    def __str__(self):
        return self.user.username + "的token:" + self.token

    class Meta:
        db_table = 'token'
        managed = True
        verbose_name = '用户token'
        verbose_name_plural = '用户token'


class UserManager(BaseUserManager):  # 自定义Manager管理器
    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, email, **kwargs):  # 创建普通用户
        kwargs['is_superuser'] = False
        return self._create_user(username, password, email, **kwargs)

    def create_superuser(self, username, password, email, **kwargs):  # 创建超级用户
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, email, **kwargs)


class User(AbstractUser):  # 自定义User
    GENDER_TYPE = (
        ("1", "男"),
        ("2", "女")
    )
    id = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=15, verbose_name="账号", unique=True)
    name = models.CharField(max_length=13, verbose_name="昵称", null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_TYPE, verbose_name="性别", null=True, blank=True)
    tel = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    email = models.EmailField(null=True, blank=True, verbose_name="邮箱")
    home_address = models.CharField(max_length=100, null=True, blank=True, verbose_name="地址")
    card_id = models.CharField(max_length=30, verbose_name="身份证", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="激活状态")
    is_staff = models.BooleanField(default=False, verbose_name="是否是员工")
    photo = models.CharField(
        max_length=512, verbose_name="学生照片", null=True, blank=True
    )
    wx_openid = models.CharField(
        max_length=128, verbose_name=u'微信标识', null=True, blank=True
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name='user',
        null=True, blank=True,
        verbose_name="班级id",
    )
    USERNAME_FIELD = 'username'  # 使用authenticate验证时使用的验证字段，可以换成其他字段，但验证字段必须是唯一的，即设置了unique=True
    REQUIRED_FIELDS = ['email']  # 创建用户时必须填写的字段，除了该列表里的字段还包括password字段以及USERNAME_FIELD中的字段
    EMAIL_FIELD = 'email'  # 发送邮件时使用的字段

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name
