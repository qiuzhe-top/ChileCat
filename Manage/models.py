from django.db import models

# Create your models here.
class Primitives(models.Model):

    title = models.CharField(max_length = 30,verbose_name = "标题")
    

    class Meta:
        verbose_name = "分类主表"
        verbose_name_plural = "分类主表"

    def __str__(self):
        return self.title

class TypePar(models.Model):

    title = models.CharField(max_length = 30,verbose_name = "标题")
    par_id = models.ForeignKey("Primitives", on_delete=models.CASCADE,verbose_name = "主表id")
    

    class Meta:
        verbose_name = "分类父表"
        verbose_name_plural = "分类父表"

    def __str__(self):  
        return self.title

class TypeChild(models.Model):

    title = models.CharField(max_length = 30,verbose_name = "标题")
    par_id = models.ForeignKey("TypeChild", on_delete=models.CASCADE,verbose_name = "父表id")

    class Meta:
        verbose_name = "分类子表"
        verbose_name_plural = "分类子表"

    def __str__(self):
        return self.title

#TODO(haijialiu): 文档有一空表
