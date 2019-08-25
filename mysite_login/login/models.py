from django.db import models

# Create your models here.
class User(models.Model):
    '''用户表'''
    gender=(
        ('mail','男'),
        ('femail','女'),
    )

    name = models.CharField(max_length=128, unique=True) #用户姓名不能相同
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender, default='男')
    c_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering =['c_time']
        verbose_name = '用户'
        verbose_name_plural = verbose_name
