#users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

import os
import uuid
import datetime
# Create your models here.

def user_image_path(instance, filename):
    ext = filename.split('.')[-1]
    if ext.lower() not in ['jpg','png','gif']:
        raise NameError("image must be jpg, png or gif")
    filename = '{}.{}'.format(uuid.uuid4().hex[:10],ext)

    if isinstance(instance, UserProfile):
        return os.path.join('users','avatar',instance.username,filename) # media/users/avatar/2/filename
    if isinstance((instance, Banner)):
        return os.path.join('users','banner',filename)

class UserProfile(AbstractUser):
    gender_choices =(
        ("male", "男"),
        ("female", "女"),
    )

    nick_name = models.CharField("昵称", max_length=50, default='')
    birthday = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=gender_choices, default='female')
    address = models.CharField('地址', max_length=100, default='')
    mobile = models.CharField('手机号', max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to=user_image_path, default='users/avatar/default.jpg', max_length=100)

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class EmailVerifyRecord(models.Model):
    send_choices =(
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update_email', '修改邮箱'),
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=send_choices, max_length=20)
    send_time = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

class Banner(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to=user_image_path, max_length=100)
    #url = models.URLField('访问地址', max_length=200) #url 图片路径？ 我觉得这里不需要
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateTimeField('添加时间', default=datetime.datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return  self.title