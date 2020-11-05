from django.db import models

# Create your models here.
class User(models.Model):
    
    user_name = models.CharField(max_length=20,verbose_name="用户名")
    pass_word = models.CharField(max_length = 20,verbose_name="用户密码")

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Token(models.Model):

    token = models.CharField(max_length=100)
    wx_openid = models.CharField(max_length = 100)
    user_id = models.OneToOneField("User", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.token

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
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

class StudentInfo(models.Model):

    student_id = models.CharField(max_length = 20,verbose_name="学号")
    grade_id = models.OneToOneField("Grade", on_delete=models.CASCADE)
    user_id = models.OneToOneField("User", verbose_name="用户", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.student_id

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'

class TeacherInfo(models.Model):

    fieldName = models.CharField(max_length = 150)
    teacher_extra_info = models.CharField(verbose_name="老师额外信息", max_length=50)
    user_id = models.OneToOneField("User", verbose_name="用户", on_delete=models.CASCADE)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '老师信息'
        verbose_name_plural = '老师信息'

class TeacherForGrade(models.Model):

    grade_id = models.ForeignKey("Grade", on_delete=models.CASCADE)
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = "教师班级关系"
        verbose_name_plural = "教师班级关系"


class Grade(models.Model):

    name = models.CharField(max_length = 20,verbose_name = "班级名称")
    college_id = models.ForeignKey("College", on_delete=models.CASCADE,verbose_name="学院id")
    
    

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = "班级"

    def __str__(self):
        return self.name

class College(models.Model):

    name = models.CharField(max_length = 50,verbose_name = "学院名称")

    class Meta:
        verbose_name = "分院"
        verbose_name_plural = "分院"

    def __str__(self):
        return self.name

class Permission(models.Model):

    #权限
    auth = (
        ("common","普通"),
        ("amdin","管理员"),
    )
    name = models.CharField(max_length = 20,verbose_name = "权限",choices = auth,default = "common")
    message = models.CharField(max_length = 50,verbose_name = "描述")
        

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = "权限"

    def __str__(self):  
        return self.name

class UserForPermission(models.Model):

    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    perm_id = models.ForeignKey("Permission", on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = "用户权限表"
        verbose_name_plural = "用户权限表"

