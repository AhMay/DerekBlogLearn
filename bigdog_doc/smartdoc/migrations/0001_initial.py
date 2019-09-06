# Generated by Django 2.2.4 on 2019-09-05 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smartdoc.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('mod_date', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '文档分类',
                'verbose_name_plural': '文档分类',
                'ordering': ['-mod_date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('mod_date', models.DateField(auto_now=True)),
                ('name', models.TextField(max_length=30, verbose_name='Product Name')),
                ('code', models.TextField(blank=True, default='', max_length=30, verbose_name='Product Code')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '产品',
                'verbose_name_plural': '产品',
                'ordering': ['-mod_date'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('mod_date', models.DateField(auto_now=True)),
                ('title', models.TextField(max_length=30, verbose_name='Title')),
                ('version_no', models.SmallIntegerField(blank=True, default=1, verbose_name='Version No.')),
                ('doc_file', models.FileField(blank=True, null=True, upload_to=smartdoc.models.user_directory_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='smartdoc.Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='smartdoc.Product')),
            ],
            options={
                'verbose_name': '文档',
                'verbose_name_plural': '文档',
                'ordering': ['-mod_date'],
            },
        ),
    ]
