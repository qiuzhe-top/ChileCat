'''
数据库模型
'''
from django.db import models
# Create your models here.
class Ask(models.Model):
    '''
    请假条
    '''
    user_id = models.ForeignKey(
        'User.User',
        on_delete=models.CASCADE,
        verbose_name = "用户id",related_name = "user_id")
    askType = (
        ("0","草稿"),
        ("1","班主任审核"), # 一级审核中
        ("2","等待二级审核"), # 二级审核中
        ("3","完成"),          # 历史
        ("4","不通过")          # 不通过
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
    grade_id = models.ForeignKey(
        'User.Grade', null=True, blank=True,
        on_delete=models.SET_NULL,verbose_name=u'班级')
    '''
        当请假条没有绑定老师数据的时候默认绑定给id为1的用户
        (这个default永远不应该被使用,unless改动了数据库亦或是前端创建请假条或者修改请假条缺损了)
        这个id不仅可以用来绑定老师(学生到班主任的审核),亦可用来绑定领导(班主任提交给领导的审核).具体按照逻辑来
    '''
    pass_id = models.ForeignKey(
        'User.User',
        verbose_name="审批老师的id1",
        on_delete=models.CASCADE,
        related_name = "pass_id",default = 1)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = "请假条"
        verbose_name_plural = "请假条"

class Audit(models.Model):
    '''
    审批记录
    '''
    user_id = models.ForeignKey("User.User", on_delete=models.CASCADE,verbose_name = "用户id")
    ask_id = models.ForeignKey(
        "Ask", null=True, blank=True,
        on_delete=models.SET_NULL,verbose_name = "请假单id")
    status = models.CharField(max_length = 21,verbose_name = "审核状态")
    explain = models.CharField(max_length = 20,verbose_name = "审核说明")
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name = "创建时间")
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name = "修改时间")

    def __str__(self):
        return "审批记录"+str(self.id)
    class Meta:
        verbose_name = "审核情况表"
        verbose_name_plural = "审核情况表"
