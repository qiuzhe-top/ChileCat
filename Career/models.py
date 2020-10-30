from django.db import models

# Create your models here.
class Career(models.Model):

    title = models.CharField(max_length = 100,verbose_name = "岗位名称")
    note = models.CharField(max_length = 300,verbose_name = "岗位介绍")
    #warning:正文限制在999字以内
    text = models.CharField(max_length = 999,verbose_name = "正文")
    source = models.CharField(max_length = 100,verbose_name = "地址")
    viewnum = models.IntegerField(verbose_name= "浏览数")
    release_time = models.TimeField(auto_now=False, auto_now_add=False,verbose_name = "发布时间")
    

    class Meta:
        verbose_name = _("Career")
        verbose_name_plural = _("Careers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Career_detail", kwargs={"pk": self.pk})
