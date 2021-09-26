'''
Author: 邹洋
Date: 2021-09-23 19:31:58
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-24 10:24:19
Description: 
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
