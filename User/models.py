'''
models
'''
from django.db import models

# Create your models here.
class User(models.Model):
    '''
    用户信息
    '''
    user_name = models.CharField(max_length=20,verbose_name="用户名")
    pass_word = models.CharField(max_length = 20,verbose_name="用户密码")

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户'
        verbose_name_plural = '用户'

# 第三方账户绑定
class Tpost(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    wx_openid = models.CharField(max_length=128, verbose_name=u'微信标识',null=True, blank=True)

    def __str__(self):
        try:
            return self.user_id.userinfo.name
        except:
            return self.user.user_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '第三方账户'
        verbose_name_plural = '第三方账户'
class Token(models.Model):
    '''
    Token
    '''
    token = models.CharField(max_length=100)
    user = models.OneToOneField("User", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user_name + "的token:" +  self.token

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户token'
        verbose_name_plural = '用户token'

class UserInfo(models.Model):
    '''
    用户信息
    '''
    name = models.CharField(max_length = 20,verbose_name="姓名")
    tel = models.CharField(max_length = 20,verbose_name="电话")
    identity = models.CharField(max_length = 20,choices=(
        ("student","学生"),
        ("teacher","老师"),
        ("college","院领导")
        ),default="student",verbose_name="身份")
    user_id = models.OneToOneField("User", on_delete=models.CASCADE,verbose_name = "用户id")


    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

class StudentInfo(models.Model):
    '''
    学生信息
    '''
    student_id = models.CharField(max_length = 20,verbose_name="学号")
    grade_id = models.ForeignKey("Grade", on_delete=models.CASCADE,verbose_name = "班级id")
    user_id = models.OneToOneField("User", verbose_name="用户", on_delete=models.CASCADE)

    def __str__(self):
        return self.student_id
    class Meta:
        db_table = ''
        managed = True
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'

class TeacherInfo(models.Model):
    '''
    老师额外信息
    '''
    teacher_extra_info = models.CharField(verbose_name="老师额外信息", max_length=50)
    user_id = models.OneToOneField("User", verbose_name="用户", on_delete=models.CASCADE)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '老师信息'
        verbose_name_plural = '老师信息'

class TeacherForGrade(models.Model):
    '''
    教师对应的班级
    '''
    grade_id = models.ForeignKey("Grade", on_delete=models.CASCADE,verbose_name="班级号")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE,verbose_name="管理者账号")

    class Meta:
        verbose_name = "教师班级关系"
        verbose_name_plural = "教师班级关系"

class TeacherForCollege(models.Model):
    '''
    教师对应的分院
    '''
    college_id = models.ForeignKey("College", on_delete=models.CASCADE,verbose_name="分院号")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE,verbose_name="管理者账号")

    class Meta:
        verbose_name = "教师院级关系"
        verbose_name_plural = "教师院级关系"


class Grade(models.Model):
    '''
    班级
    '''
    name = models.CharField(max_length = 20,verbose_name = "班级号")
    college_id = models.ForeignKey("College", on_delete=models.CASCADE,verbose_name="学院")

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = "班级"

    def __str__(self):
        return self.name

class College(models.Model):
    '''
    分院
    '''
    name = models.CharField(max_length = 50,verbose_name = "学院名称")

    class Meta:
        verbose_name = "分院"
        verbose_name_plural = "分院"

    def __str__(self):
        return self.name

class Permission(models.Model):
    '''
    权限
    '''

    name = models.CharField(max_length = 20)
    message = models.CharField(max_length = 50,verbose_name = "描述")

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = "权限"

    def __str__(self):
        return self.name

class UserForPermission(models.Model):
    '''
    用户权限
    '''
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    perm_id = models.ForeignKey("Permission", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "用户权限表"
        verbose_name_plural = "用户权限表"
