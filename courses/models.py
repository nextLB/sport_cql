from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    SPORT_CHOICES = [
        ('basketball', '篮球'),
        ('badminton', '羽毛球'),
        ('tennis', '网球'),
        ('football', '足球'),
        ('swimming', '游泳'),
        ('fitness', '健身'),
    ]
    
    STATUS_CHOICES = [
        ('open', '开放报名'),
        ('full', '已满员'),
        ('ongoing', '进行中'),
        ('completed', '已结束'),
        ('cancelled', '已取消'),
    ]
    
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='教练')
    venue_space = models.ForeignKey('venues.VenueSpace', on_delete=models.CASCADE, related_name='courses', verbose_name='场地')
    course_name = models.CharField('课程名称', max_length=100)
    sport_type = models.CharField('运动类型', max_length=20, choices=SPORT_CHOICES)
    description = models.TextField('课程描述')
    price = models.DecimalField('价格(元/人)', max_digits=10, decimal_places=2)
    max_participants = models.IntegerField('最大人数', default=10)
    current_participants = models.IntegerField('当前人数', default=0)
    
    start_date = models.DateField('开始日期')
    end_date = models.DateField('结束日期')
    start_time = models.TimeField('开始时间')
    end_time = models.TimeField('结束时间')
    recurring_days = models.CharField('重复日期(周一到周日用0-6表示)', max_length=20, blank=True, default='')
    
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'courses'
        verbose_name = '训练课程'
        verbose_name_plural = '训练课程'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.coach.username} - {self.course_name}"
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, '未知')
    
    @property
    def available_spots(self):
        return self.max_participants - self.current_participants
    
    @property
    def is_full(self):
        return self.current_participants >= self.max_participants


class CourseEnrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='课程')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name='学员')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('报名时间', auto_now_add=True)
    
    class Meta:
        db_table = 'course_enrollments'
        verbose_name = '课程报名'
        verbose_name_plural = '课程报名'
        unique_together = ['course', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.course_name}"
