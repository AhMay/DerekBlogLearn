# Generated by Django 2.2.4 on 2019-09-05 07:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_auto_20190905_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='articles_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]