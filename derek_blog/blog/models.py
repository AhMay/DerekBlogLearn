from django.urls import reverse
from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    '''根据博客园，Category是由名字和描述组成的。且一篇文章不一定一定要由类别'''
    name = models.CharField('分类',max_length=128)
    description = models.TextField(verbose_name='描述',max_length=1000,blank=True,default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

class Tag(models.Model):
    '''每篇文章可以有多个标签(多个标签之间用;隔开)'''
    name = models.CharField('标签', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

class Entry(models.Model):
    '''文章'''
    title = models.CharField('文章标题', max_length=128) #必须
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='blog_img', null=True, blank=True, verbose_name='博客配图') #摘要右侧图？
    body = models.TextField('正文') #必须
    abstract = models.TextField('摘要', max_length=256, null=True, blank=True) #非必需
    visiting = models.PositiveIntegerField('访问量', default=0) #阅读
    category = models.ManyToManyField('Category', verbose_name='博客分类',blank=True,null=True) #博客园分类非必需，多对多 一个文章可以属于多个类别
    tags = models.ManyToManyField('Tag', verbose_name='标签',blank=True,null=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modifyed_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'blog_id':self.id})

    def increase_visiting(self):
        #访问量+1
        self.visiting +=1
        self.save(update_fields=['visiting']) #只保存某个字段

    class Meta:
        ordering = ['-created_time']
        verbose_name = '博客正文'
        verbose_name_plural = verbose_name


