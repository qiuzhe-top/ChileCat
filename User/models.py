from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=20,blank=True, null=True)
    pass_word = models.CharField(max_length = 20)
    
    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'