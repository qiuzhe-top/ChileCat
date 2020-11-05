'''
数据库模型
'''
from django.db import models

# Create your models here.
class Ask(models.Model):
    '''
    请假条
    '''
    user_id = models.ForeignKey("User.user", on_delete=models.CASCADE,verbose_name = "用户id")
    askType = (
        ("0","草稿"),
        ("1","刚刚提交"),
        ("2","班主任审核通过"),
        ("3","上级通过"),
    )
    status = models.CharField(max_length = 20,choices = askType,verbose_name = "状态",default = "0")
    contact_info = models.CharField(max_length = 20,verbose_name = "联系信息")
    ask_type = models.CharField(max_length = 20,choices = (
        ("out","外出"),
        ("leave","事假"),
        ("other","其他")
        ),verbose_name = "状态",default = "out")
    reason = models.CharField(max_length = 50,verbose_name = "理由")
    place = models.CharField(max_length = 50,verbose_name = "地点")
    ask_state = models.CharField(max_length = 2,verbose_name = "请假状态")
    start_time = models.TimeField(auto_now=False, auto_now_add=False,verbose_name = "开始时间")
    end_time = models.TimeField(auto_now=False, auto_now_add=False,verbose_name = "结束时间")
    created_time = models.TimeField(auto_now=False, auto_now_add=True,verbose_name = "创建时间")
    modify_time = models.TimeField(auto_now=True, auto_now_add=False,verbose_name = "修改时间")
    class Meta:
        verbose_name = "请假条"
        verbose_name_plural = "请假条"

class Audit(models.Model):

    user_id = models.ForeignKey("User.User", on_delete=models.CASCADE,verbose_name = "用户id")
    ask_id = models.ForeignKey("Ask", on_delete=models.CASCADE,verbose_name = "请假单id")
    level = models.IntegerField(verbose_name = "等级")
    note = models.CharField(max_length = 20,verbose_name = "备注")
    created_time = models.TimeField(auto_now=False, auto_now_add=False,verbose_name = "创建时间")
    modify_time = models.TimeField(auto_now=False, auto_now_add=False,verbose_name = "修改时间")
    class Meta:
        verbose_name = "审核情况表"
        verbose_name_plural = "审核情况表"
