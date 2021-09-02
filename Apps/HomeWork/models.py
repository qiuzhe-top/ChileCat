'''
Author: 邹洋
Date: 2021-09-02 14:35:30
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-02 14:57:20
Description: 
'''
from django.db import models
from django.contrib.auth.models import User
from cool.admin import admin_register



admin_register()
class HomeWork(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'名称')
    message = models.CharField(max_length=1000, verbose_name=u'备注')
    admin = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u'作业管理员')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "作业任务"
admin_register()
class DoWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    file = models.TextField()

    def __str__(self):
        return self.work.name

    class Meta:
        verbose_name_plural = "作业完成情况"

