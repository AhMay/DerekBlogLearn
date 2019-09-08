from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import uuid
import os
def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    sub_folder = 'avatar'
    if ext.lower() not in ['jpg', 'png','gif']:
        raise NameError("user avatar must be picture")
    return os.path.join(str(instance.user.id), sub_folder, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    org = models.CharField('Organization', max_length=128, blank=True)
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, default=os.path.join('avatar','default.jpg'), verbose_name='头像')
    join_date = models.DateTimeField('Join date', blank=True, null=True, auto_now_add=True)
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return '{}"s profle'.format(self.user.username)
