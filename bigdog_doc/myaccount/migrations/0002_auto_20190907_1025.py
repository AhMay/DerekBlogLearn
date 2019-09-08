# Generated by Django 2.2.4 on 2019-09-07 02:25

from django.db import migrations, models
import myaccount.models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='avatar\\default.jpg', upload_to=myaccount.models.user_avatar_path, verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='join_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Join date'),
        ),
    ]
