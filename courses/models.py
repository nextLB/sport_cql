from django.db import models
from django.conf import settings
from venues.models import Venue


class Coach(models.Model):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    STATUS_CHOICES = (
        ('active', '在职'),
        ('inactive', '离职'),
    )

    name = models.CharField(max_length=50, verbose_name='教练姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    avatar = models.ImageField(upload_to='coaches/', default='coaches/default.jpg', verbose_name='头像')
    speciality = models.CharField(max_length=200, verbose_name='擅长项目')
    description = models.TextField(blank=True, verbose_name='个人简介')
    experience = models.IntegerField(default=0, verbose_name='教龄(年)')
    certificate = models.CharField(max_length=200, blank=True, verbose_name='资质证书')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'coaches'
        verbose_name = '教练'
        verbose_name_plural = '教练'

    def __str__(self):
        return self.name


class Course(models.Model):
    COURSE_TYPE_CHOICES = (
        ('football', '足球'),
        ('basketball', '篮球'),
        ('tennis', '网球'),
        ('badminton', '羽毛球'),
        ('swimming', '游泳'),
        ('table_tennis', '乒乓球'),
        ('fitness', '健身'),
        ('other', '其他'),
    )
    STATUS_CHOICES = (
        ('enrolling', '报名中'),
        ('in_progress', '进行中'),
        ('completed', '已结课'),
        ('cancelled', '已取消'),
    )

    name = models.CharField(max_length=100, verbose_name='课程名称')
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='courses', verbose_name='授课教练')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='courses', verbose_name='上课场馆')
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, verbose_name='课程类型')
    description = models.TextField(blank=True, verbose_name='课程描述')
    max_students = models.IntegerField(default=20, verbose_name='最大人数')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='课程价格')
    start_date = models.DateField(verbose_name='开课日期')
    end_date = models.DateField(verbose_name='结课日期')
    schedule = models.CharField(max_length=200, verbose_name='上课时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolling', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'courses'
        verbose_name = '课程'
        verbose_name_plural = '课程'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def enrolled_count(self):
        return self.enrollments.filter(status='enrolled').count()


class CourseEnrollment(models.Model):
    STATUS_CHOICES = (
        ('enrolled', '已报名'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='课程')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments', verbose_name='学员')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='报名时间')

    class Meta:
        db_table = 'course_enrollments'
        verbose_name = '课程报名'
        verbose_name_plural = '课程报名'
        unique_together = ['course', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"
