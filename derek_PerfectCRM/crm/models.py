#crm/model.py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=64, unique=True) #不能重 不同角色可以做不同的事情
    menus = models.ManyToManyField('Menus', blank=True, null=True, verbose_name='动态菜单')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='角色'
        verbose_name_plural =verbose_name

class UserProfile(models.Model):
    '''用户信息表'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField('姓名', max_length=64)
    role = models.ManyToManyField(Role, blank=True, null=True) #一个用户可以有多个角色，一个角色可以对应多个用户

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='用户'
        verbose_name_plural =verbose_name

class CustomerInfo(models.Model):
    '''客户信息表'''
    contact_type_choices = (
        (0,'qq'),
        (1,'微信'),
        (2,'手机'),
    )
    source_choices = (
        (0,'qq群'),
        (1, '51CTO'),
        (2,'百度推广'),
        (3,'知乎'),
        (4,'转介绍'),
        (5, '其他'),
    )
    status_choices = (
        (0,'未报名'),
        (1,'已报名'),
        (2,'已退学'),
    )
    name = models.CharField('姓名', max_length=64, default='')
    contact_type = models.SmallIntegerField(choices=contact_type_choices, default=0)
    contact = models.CharField('联系方式', max_length=64, unique=True)
    source = models.SmallIntegerField('客户来源', choices=source_choices)
    referral_from = models.ForeignKey('self', blank=True, null=True, verbose_name='转介绍人', on_delete=models.CASCADE)
    #可以咨询多个课程
    consult_courses = models.ManyToManyField('Course', verbose_name='咨询课程')
    consult_content = models.TextField('咨询内容')
    status = models.SmallIntegerField('客户状态', choices=status_choices)
    consultant = models.ForeignKey(UserProfile, verbose_name='课程顾问', on_delete=models.CASCADE) #需要根据角色过滤么？
    date = models.DateField('创建的时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural =verbose_name

class Student(models.Model):
    '''学员表'''
    customer = models.ForeignKey(CustomerInfo, verbose_name='客户', on_delete=models.CASCADE) #每个学员都是客户转过来的
    class_grades = models.ManyToManyField('ClassList', verbose_name='班级') #一个学员可以在多个班学习，一个班可以对应多个学生

    def __str__(self):
        return self.customer

    class Meta:
        verbose_name='学员'
        verbose_name_plural =verbose_name

class CustomerFollowUp(models.Model):
    '''客户跟踪记录表'''
    status_choices = (
        (0,'近期无报名计划'),
        (1,'一个月内报名'),
        (2,'半个月报名'),
        (3,'已报名'),
    )
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    content = models.TextField('跟踪内容')
    user = models.ForeignKey(UserProfile, verbose_name='跟进人', on_delete=models.CASCADE)
    status = models.SmallIntegerField('客户状态', choices=status_choices)
    date = models.DateField('创建时间', auto_now_add=True)

    def __str__(self):
        return  self.customer

    class Meta:
        verbose_name='客户跟踪记录'
        verbose_name_plural =verbose_name

class Course(models.Model):
    '''课程表'''
    name = models.CharField('课程名', max_length=64, unique=True)
    #价格必需为整数
    price = models.PositiveSmallIntegerField('价格')
    period = models.PositiveSmallIntegerField('课程周期(月)', default=5)
    outline = models.TextField('大纲',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='课程'
        verbose_name_plural =verbose_name

class ClassList(models.Model):
    '''班级列表'''
    class_type_choices =(
        (0,'脱产'),
        (1,'周末'),
        (2,'网络班'),
    )
    branch = models.ForeignKey('Branch', verbose_name='校区', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE) #一个班级只能有一个课程
    class_type = models.SmallIntegerField('班级类型', choices=class_type_choices, default=0)
    semester = models.SmallIntegerField('学期',)
    teachers = models.ManyToManyField(UserProfile, verbose_name='讲师') #一个班可以有多个讲师，一个讲师可以教多个班
    start_date = models.DateField('开班日期',)
    graduate_date = models.DateField('毕业日期', blank=True, null=True) #毕业日期因为不固定，所以可以为空
    #还应该有上课的时间段

    def __str__(self):
        return "{}({})期".format(self.course.name, self.semester)

    class Meta:
        verbose_name='班级'
        verbose_name_plural =verbose_name
        unique_together = ('branch','class_type','course','semester')

class CourseRecord(models.Model):
    '''上课记录'''
    class_grade = models.ForeignKey(ClassList, verbose_name='上课班级', on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField('课程节次')
    teacher = models.ForeignKey(UserProfile, verbose_name='讲师', on_delete=models.CASCADE)
    title = models.CharField('本节主题', max_length=64)
    content = models.TextField('本节内容')
    has_homework = models.BooleanField('本节有作业', default=True)
    homework = models.TextField('作业需求', blank=True, null=True)
    date = models.DateField('创建时间', auto_now_add=True)

    def __str__(self):
        return "{}第({})节" % (self.class_grade, self.day_num)

    class Meta:
        unique_together = ('class_grade','day_num')
        verbose_name ='上课记录'
        verbose_name_plural = verbose_name

class StudyRecord(models.Model):
    '''学习记录'''
    score_choices=(
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (75, 'B-'),
        (70, 'C+'),
        (60, 'C'),
        (40, 'C-'),
        (-50, 'D'),
        (0, 'N/A'),  # not avaliable
        (-100, 'COPY'),
    )
    show_choices =(
        (0,'缺勤'),
        (1,'已签到'),
        (2,'迟到'),
        (3,'早退'),
    )
    course_record = models.ForeignKey(CourseRecord, verbose_name='课程', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name='学生', on_delete=models.CASCADE)
    score = models.SmallIntegerField('得分', choices=score_choices, default=0)
    show_status = models.SmallIntegerField('出勤', choices=show_choices, default=1)
    note = models.TextField('成绩备注', blank=True, null=True)
    date = models.DateField('创建的时间', auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(self.course_record, self.student, self.score)

    class Meta:
        verbose_name ='学生学习记录'
        verbose_name_plural = verbose_name

class Branch(models.Model):
    '''校区分支'''
    name = models.CharField('校区名', max_length=64, unique=True)
    addr = models.CharField('地址', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ='校区'
        verbose_name_plural = verbose_name

#销售，学生，讲师访问页面时，显示的应该是对应角色的菜单，所以需要动态生成菜单
class Menus(models.Model):
    '''动态菜单'''
    url_type_choices =(
        (0,'absolute'),
        (1,'dynamic'),
    )
    name = models.CharField(max_length=64)
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ='菜单项'
        verbose_name_plural = verbose_name
        unique_together =('name','url_name')

