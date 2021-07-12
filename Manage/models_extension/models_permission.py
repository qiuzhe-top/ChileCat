'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-11 13:36:49
Description: 
'''
"""授权数据模型"""
from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.
class ApiPermission(models.Model):
    """接口访问权限"""
    is_verify = models.IntegerField(verbose_name=u'接口类型', choices=(
        (1, "公开须登录"),
        (2, "公开"),
        (3, "权限"),
    ), default=False)
    
    permission = models.OneToOneField(
        Permission, on_delete=models.CASCADE,
        verbose_name="权限",
        related_name="api_permission",
        null=True,
        blank=True
    )

    class Meta:
        """Meta definition for ApiPermission."""

        verbose_name = 'API权限'
        verbose_name_plural = 'API权限'

    def __str__(self):
        """Unicode representation of ApiPermission."""
        return self.permission.name


class ElementPermission(models.Model):
    """元素显示权限"""

    name = models.CharField(max_length=50, verbose_name="名称")
    per_id = models.OneToOneField(
        Permission, on_delete=models.CASCADE,
        verbose_name="权限",
        related_name="element_permission"
    )

    class Meta:
        """Meta definition for ElementPermission."""

        verbose_name = 'ElementPermission'
        verbose_name_plural = '元素显示权限'

    def __str__(self):
        """Unicode representation of ElementPermission."""
        return self.name


class OperatePermission(models.Model):
    """操作权限"""

    permission = models.OneToOneField(
        Permission,
        on_delete=models.CASCADE,
        verbose_name="权限",
        related_name="operate_permission"
    )

    class Meta:
        """Meta definition for OperatePermission."""

        verbose_name = '操作权限记录'
        verbose_name_plural = '操作权限记录'

    def __str__(self):
        """Unicode representation of OperatePermission."""
        return self.permission.name
