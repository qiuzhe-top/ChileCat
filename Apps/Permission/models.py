'''授权数据模型'''
from django.db import models
from django.contrib.auth.models import Permission
# Create your models here.


# class Role(models.Model):
#     """角色分类表"""
#     name = models.CharField(max_length = 150,verbose_name="职位")
#     role_permit = models.ManyToManyField(
#         "PermissionsExtension",verbose_name="角色权限",blank=True,related_name="role"
#         )
#     class Meta:
#         """Meta definition for Role."""

#         verbose_name = '角色表'
#         verbose_name_plural = '角色表'

#     def __str__(self):
#         """Unicode representation of Role."""
#         return self.name

# class PermissionsExtension(models.Model):
#     """权限表."""
#     GENDER_CHOICES = (
#         (u'1', u'API权限'),
#         (u'2', u'元素显示权限'),
#     )
#     permission  = models.OneToOneField(DjangoPermission,on_delete=models.CASCADE,verbose_name=u'权限')
#     per_type = models.CharField(max_length = 150,verbose_name="类型",default="0",choices=GENDER_CHOICES)
#     description = models.CharField(max_length = 150,verbose_name="描述",blank=True,null=True)

#     class Meta:
#         """Meta definition for Permission."""

#         verbose_name = '权限'
#         verbose_name_plural = '权限'

#     def __str__(self):
#         """Unicode representation of Permission."""
#         return self.permission.name

class ApiPermission(models.Model):
    """接口访问权限"""
    
        
    is_verify = models.BooleanField(verbose_name="接口类型",choices=(
            (False,"权限接口"),
            (True,"公开接口"),
        ),default=False)
    
    permission = models.OneToOneField(
        Permission, on_delete=models.CASCADE,
        verbose_name="权限",
        related_name="apipermission",
        null=True,
        blank=True
        )

    class Meta:
        """Meta definition for ApiPermission."""

        verbose_name = 'API权限'
        verbose_name_plural = 'API权限'

    def __str__(self):
        """Unicode representation of ApiPermission."""
        return self.permission.name

class ElementPermission(models.Model):
    """元素显示权限"""

    name = models.CharField(max_length = 50,verbose_name="名称")
    per_id = models.OneToOneField(
        Permission, on_delete=models.CASCADE,
        verbose_name="权限",
        related_name="elementpermission"
        )


    class Meta:
        """Meta definition for ElementPermission."""

        verbose_name = 'ElementPermission'
        verbose_name_plural = '元素显示权限'

    def __str__(self):
        """Unicode representation of ElementPermission."""
        return self.name

class OperatePermission(models.Model):
    """操作权限"""

    permission = models.OneToOneField(
        Permission,
        on_delete=models.CASCADE,
        verbose_name="权限",
        related_name="operatepermission"
        )


    class Meta:
        """Meta definition for OperatePermission."""

        verbose_name = '操作权限记录'
        verbose_name_plural = '操作权限记录'

    def __str__(self):
        """Unicode representation of OperatePermission."""
        return self.permission.name
class WriteList(models.Model):
    """白名单."""

    name = models.CharField(max_length = 150,verbose_name="内容")
    flag = models.CharField(max_length = 20,verbose_name="类型")

    class Meta:
        """Meta definition for WriteList."""

        verbose_name = 'WriteList'
        verbose_name_plural = 'WriteLists'

    def __str__(self):
        """Unicode representation of WriteList."""
        return self.name
