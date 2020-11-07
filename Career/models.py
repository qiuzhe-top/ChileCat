'''
/models
'''
from django.db import models

# Create your models here.
class Career(models.Model):
    '''
    职业说明数据库
    '''
    title = models.CharField(max_length = 100,verbose_name = "岗位名称")
    note = models.CharField(max_length = 300,verbose_name = "岗位介绍")
    #warning:正文限制在999字以内
    text = models.CharField(max_length = 999,verbose_name = "正文")
    source = models.CharField(max_length = 100,verbose_name = "地址")
    viewnum = models.IntegerField(verbose_name= "浏览数",default = 0)
    release_time = models.DateTimeField(auto_now=False, auto_now_add=False,verbose_name = "发布时间")


    class Meta:
        verbose_name = "就业信息表"
        verbose_name_plural = "就业信息表"
        ordering = ['id']

    def __str__(self):
        return self.title
        