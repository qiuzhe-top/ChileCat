'''
Author: 邹洋
Date: 2022-02-06 21:30:49
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-06 21:45:49
Description: 公共模型
'''

from django.db import models


class ActiveManager(models.Manager):
    
    def filter(self, *args, **kwargs):
        if not kwargs.get('is_active', True): # 如果需要查看所有数据，
            kwargs.pop('is_active')
        else:
            kwargs['is_active'] = True
        return super(models.Manager, self).filter(*args, **kwargs)


class ActiveBase(models.Model):
    '''
    软删除基类 数据是否激活可用
    '''
    objects = ActiveManager()
    is_active = models.BooleanField(default=True)

    def delete(self, using=None, soft=True, *args, **kwargs):
        if soft:
            self.is_active = False
            self.save()
        else:
            return super(models.Manager, self).delete(using=using, *args, **kwargs)

    class Meta:
        abstract = True 


class TimeClass():
    star_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建日期')
    last_time = models.DateTimeField(auto_now=True, verbose_name=u'最后修改日期')
