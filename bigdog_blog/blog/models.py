from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify

from ckeditor_uploader.fields import RichTextUploadingField

from datetime import datetime

# Create your models here.
class Article(models.Model):
    '''文章模型'''
    STATUS_CHOICES =(
        ('d', '草稿'),
        ('p','发表'),
    )

    title = models.CharField('标题', max_length=200 )
    slug = models.SlugField('slug', max_length=60, blank=True) #slug 最大的作用就是便于读者和搜索引擎之间从url中了解文章大概包含了什么内容
   # body = models.TextField('正文')
    body = RichTextUploadingField('正文')
    pub_date = models.DateTimeField('发布时间', null=True, blank=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    mod_date = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='d')
    views = models.PositiveIntegerField('浏览量', default=0)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    users_like = models.ManyToManyField(User,related_name='articles_liked', blank=True)
    category = models.ManyToManyField('Category',verbose_name='分类', blank=True, null=True) #多对多
    tags = models.ManyToManyField('Tag', verbose_name='标签', blank=True, null=True) #多对多

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id or not self.slug: #还没有保存，slug 还没有生成
            self.slug = slugify(unidecode(self.title)) #中文标题
        super().save(*args,**kwargs)

    #当模型的各个字段之间并不彼此独立时，可以添加自定义的clean方法
    def clean(self):
        if self.status == 'd' and self.pub_date is not None:
            self.pub_date = None
        if self.status == 'p' and self.pub_date is None:
            self.pub_date = datetime.now()

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.pk, self.slug])

    def viewed(self):
        self.views +=1
        self.save(update_fields=['views'])

    def published(self):
        self.status = 'p'
        self.pub_date = datetime.now()
        self.save(update_fields=['status','pub_date'])

    class Meta:
        ordering = ['-pub_date']
        verbose_name ='文章'
        verbose_name_plural = verbose_name

class Category(models.Model):
    '''文章分类'''
    name = models.CharField('分类名', max_length=30)
    slug = models.SlugField('slug', max_length=40,blank=True)
    parent_category = models.ForeignKey('self', verbose_name='父级分类', blank=True, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return  reverse('blog:category_detail', args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(args, kwargs)

    def has_child(self):
        if self.category_set.all().count() >0: # 外键
            return True

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '分类'
        verbose_name_plural = verbose_name

class Tag(models.Model):
    '''文章标签'''
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField('slug', max_length=40,blank=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('blog:tag_detail', args=[self.name])

    def get_article_count(self):
        return Article.objects.filter(tags__slug=self.slug).count() #slug 应该不为空

    def save(self,*args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args,**kwargs)

    class Meta:
        ordering =['name']
        verbose_name = '标签'
        verbose_name_plural = verbose_name