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
        ("1","等待一级审核"), # 一级审核中
        ("2","等待二级审核"), # 二级审核中
        ("3","完成")          # 历史
    )
    status = models.CharField(max_length = 20,choices = askType,verbose_name = "审核状态",default = "0")
    contact_info = models.CharField(max_length = 20,verbose_name = "联系信息")
    ask_type = models.CharField(max_length = 20,choices = (
        ("0","外出"),
        ("1","事假"),
        ("2","其他")
        ),verbose_name = "状态",default = "1")
    reason = models.CharField(max_length = 50,verbose_name = "理由")
    place = models.CharField(max_length = 50,verbose_name = "地点")
    ask_state = models.CharField(max_length = 5,verbose_name = "是否完成",choices = (
        ("1","完成"),
        ("0","未完成")
        ),default = "0")
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False,verbose_name = "开始时间")
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False,verbose_name = "结束时间")
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name = "创建时间")
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name = "修改时间")
 
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = "请假条"
        verbose_name_plural = "请假条"

class Audit(models.Model):

    user_id = models.ForeignKey("User.User", on_delete=models.CASCADE,verbose_name = "用户id")
    ask_id = models.ForeignKey("Ask", on_delete=models.CASCADE,verbose_name = "请假单id")
    level = models.IntegerField(verbose_name = "等级")
    note = models.CharField(max_length = 20,verbose_name = "备注")
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name = "创建时间")
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name = "修改时间")
    class Meta:
        verbose_name = "审核情况表"
        verbose_name_plural = "审核情况表"
