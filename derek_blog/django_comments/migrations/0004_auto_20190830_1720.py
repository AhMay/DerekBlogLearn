# Generated by Django 2.2.4 on 2019-08-30 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_comments', '0003_add_submit_date_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_title',
            field=models.CharField(blank=True, default='无标题', max_length=256, null=True, verbose_name='评论标题'),
        ),
        migrations.AddField(
            model_name='comment',
            name='level',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='评论层级'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_comment', to='django_comments.Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_img',
            field=models.ImageField(blank=True, null=True, upload_to='user_images', verbose_name='用户图像'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='site',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_email',
            field=models.EmailField(blank=True, default='xxx@xxx.com', max_length=254, null=True, verbose_name="user's email address"),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_url',
            field=models.URLField(blank=True, default='https://xxx.xxx.xxx.xxxx', null=True, verbose_name="user's URL"),
        ),
    ]
