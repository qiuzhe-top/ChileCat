from django.db import models

# Create your models here.
class Career(models.Model):
    '''
    文章
    '''
    title = models.CharField(max_length = 100,verbose_name = "标题")
    note = models.CharField(max_length = 300,verbose_name = "介绍")
    text  = models.TextField(verbose_name=u'正文')
    source = models.CharField(max_length = 100,verbose_name = "地址",null=True, blank=True)
    viewnum = models.IntegerField(verbose_name= "浏览数",default = 0)
    star_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建日期')
    last_time = models.DateTimeField(auto_now=True,verbose_name=u'最后修改日期')
    classify = models.ForeignKey('TypeChild',on_delete=models.CASCADE,verbose_name=u'分类')
    

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['id']

    def __str__(self):
        return self.title
class Primitives(models.Model):

    title = models.CharField(max_length = 30,verbose_name = "标题")

    class Meta:
        verbose_name = "分类主表"
        verbose_name_plural = "分类主表"

    def __str__(self):
        return self.title

class TypePar(models.Model):

    title = models.CharField(max_length = 30,verbose_name = "标题")
    par_id = models.ForeignKey(
        "Primitives", on_delete=models.CASCADE,verbose_name = "主表id" ,null=True, blank=True
        )

    class Meta:
        verbose_name = "分类父表"
        verbose_name_plural = "分类父表"

    def __str__(self):  
        return self.title

class TypeChild(models.Model):

    title = models.CharField(max_length = 30,verbose_name = "标题")
    par_id = models.ForeignKey("TypePar", on_delete=models.CASCADE,verbose_name = "父表id")

    class Meta:
        verbose_name = "分类子表"
        verbose_name_plural = "分类子表"

    def __str__(self):
        return self.title
