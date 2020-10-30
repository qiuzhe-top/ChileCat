from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=20,verbose_name="用户名")
    pass_word = models.CharField(max_length = 20,verbose_name="用户密码")

    def __str__(self):
        return user_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
class Token(models.Model):
    token = models.CharField(max_length=100)
    wx_token = models.CharField(max_length = 100)
    user_id = models.OneToOneField("User", on_delete=models.CASCADE)
    
    def __str__(self):
        return token

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户token'
        verbose_name_plural = '用户token'

class UserInfo(models.Model):
    name = models.CharField(max_length = 20,verbose_name="姓名")
    tel = models.CharField(max_length = 20,verbose_name="电话")
    identity = models.CharField(max_length = 20,choices=(("student","学生"),("teacher","老师")),default="student",verbose_name="身份")
    user_id = models.OneToOneField("User", on_delete=models.CASCADE)
    

    def __str__(self):
        return name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

class StudentInfo(models.Model):
    student_id = models.CharField(max_length = 20,verbose_name="学号")
    grade_id = models.CharField(max_length = 20,verbose_name="班级号")
    user_id = models.OneToOneField("User", verbose_name=_(""), on_delete=models.CASCADE)
    
    def __str__(self):
        return student_id

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'

class TeacherInfo(models.Model):
    fieldName = models.CharField(max_length = 150)
    teacher_extra_info = models.CharField(verbose_name=_("老师额外信息"), max_length=50)
    

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '老师信息'
        verbose_name_plural = '老师信息'