from django.db import models

# Create your models here.
class UserInfo(models.Model):
    USER_TYPE = (
        (1,'普通用户'),
        (2,'VIP'),
        (3,'SVIP')
    )

    user_type = models.IntegerField(choices=USER_TYPE)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    group = models.ForeignKey('UserGroup', on_delete=models.CASCADE)
    roles = models.ManyToManyField('Role')

class UserToken(models.Model):
    user = models.OneToOneField(UserInfo,on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

class UserGroup(models.Model):
    title = models.CharField(max_length=32)

class Role(models.Model):
    title = models.CharField(max_length=32)