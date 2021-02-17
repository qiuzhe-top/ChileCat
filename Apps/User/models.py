'''
models
'''
from django.db import models
from django.contrib.auth.models import User


# 第三方账户绑定
class Tpost(models.Model):
    """第三方账户绑定"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wx_openid = models.CharField(max_length=128, verbose_name=u'微信标识', null=True, blank=True)

    def __str__(self):
        try:
            return self.user_id.userinfo.name
        except:
            return self.user.username

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '第三方账户'
        verbose_name_plural = '第三方账户'


class Token(models.Model):
    """
    Token
    """
    token = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")

    def __str__(self):
        return self.user.username + "的token:" + self.token

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户token'
        verbose_name_plural = '用户token'


class UserInfo(models.Model):
    """
    用户信息
    """
    name = models.CharField(max_length=20, verbose_name="姓名")
    tel = models.CharField(max_length=20, verbose_name="电话", blank=True, null=True)
    identity = models.CharField(max_length=20, choices=(
        ("student", "学生"),
        ("teacher", "老师"),
        ("college", "院领导")
    ), default="student", verbose_name="身份信息")
    # 头像 https://a.jgp
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户id")

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


class StudentInfo(models.Model):
    """
    学生信息
    """
    grade_id = models.ForeignKey(
        "Grade", on_delete=models.CASCADE,
        verbose_name="班级id", related_name="studentgrade"
    )
    user_id = models.OneToOneField(User, verbose_name="用户", on_delete=models.CASCADE)

    # 家长电话
    def __str__(self):
        return self.user_id.username

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'


class TeacherInfo(models.Model):
    """
    老师额外信息
    """
    teacher_extra_info = models.CharField(verbose_name="老师额外信息", max_length=50)
    user_id = models.OneToOneField(User, verbose_name="用户", on_delete=models.CASCADE)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '老师信息'
        verbose_name_plural = '老师信息'


class TeacherForGrade(models.Model):
    """
    教师对应的班级
    """
    grade_id = models.OneToOneField(
        "Grade", on_delete=models.CASCADE, verbose_name="班级号", related_name="related_to_teacher"
    )
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="管理者账号", related_name="related_to_grade")

    class Meta:
        verbose_name = "教师班级关系"
        verbose_name_plural = "教师班级关系"

    def __str__(self):
        return self.user_id.userinfo.name + "->" + self.grade_id.name


class TeacherForCollege(models.Model):
    '''
    教师对应的分院
    '''
    college_id = models.ForeignKey("College", on_delete=models.CASCADE, verbose_name="分院号")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="管理者账号")

    class Meta:
        verbose_name = "教师院级关系"
        verbose_name_plural = "教师院级关系"


class Grade(models.Model):
    '''
    班级
    '''
    name = models.CharField(max_length=20, verbose_name="班级号", unique=True)
    college_id = models.ForeignKey("College", on_delete=models.CASCADE, verbose_name="学院")

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = "班级"

    def __str__(self):
        return self.name


class College(models.Model):
    '''
    分院
    '''
    name = models.CharField(max_length=50, verbose_name="学院名称")

    class Meta:
        verbose_name = "分院"
        verbose_name_plural = "分院"

    def __str__(self):
        return self.name


# 心情监测
class UserMood(models.Model):
    '''
    心情监测
    '''
    mod_level = models.CharField(max_length=2, verbose_name=u'心情等级')
    message = models.CharField(max_length=9999, verbose_name=u'想说的话')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'学生用户')
    Grade = models.ForeignKey("Grade", on_delete=models.CASCADE, verbose_name=u'班级')
    star_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建日期')

    def riqi(self):
        '''日期'''
        return '666'

    # 设置方法字段在admin中显示的标题
    riqi.short_description = '发布日期'

    class Meta:
        verbose_name = "心情监测表"
        verbose_name_plural = "心情监测表"
