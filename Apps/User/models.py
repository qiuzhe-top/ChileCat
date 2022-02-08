'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 11:11:17
Description: 
'''

from  SchoolInformation.models import *
from cool.admin import admin_register
from django.conf import settings
from django.db import models


# 第三方账户绑定
class Token(models.Model):
    """
    Token
    """

    token = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="用户")

    def __str__(self):
        return self.user.username + "的token:" + self.token

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户token'
        verbose_name_plural = '用户token'
