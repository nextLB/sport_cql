from django.db import models
from django.contrib.auth import get_user_model
from venues.models import VenueSpace

User = get_user_model()


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('confirmed', '已确认'),
        ('rejected', '已拒绝'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name='预约用户')
    space = models.ForeignKey(VenueSpace, on_delete=models.CASCADE, related_name='bookings', verbose_name='预约场地')
    booking_date = models.DateField('预约日期')
    time_slot = models.CharField('时间段', max_length=50)
    contact_phone = models.CharField('联系电话', max_length=20)
    remark = models.TextField('备注', blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    reject_reason = models.TextField('拒绝理由', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        verbose_name = '预约'
        verbose_name_plural = '预约'
        ordering = ['-created_at']
        unique_together = ['space', 'booking_date', 'time_slot']
    
    def __str__(self):
        return f"{self.user.username} - {self.space.name} - {self.booking_date} {self.time_slot}"
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, '未知')
    
    @property
    def can_cancel(self):
        return self.status in ['pending', 'confirmed']
    
    @property
    def can_rate(self):
        return self.status == 'completed' and not hasattr(self, 'rating')


class BookingRating(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='rating', verbose_name='预约')
    score = models.IntegerField('评分', choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField('评价内容', blank=True)
    created_at = models.DateTimeField('评价时间', auto_now_add=True)
    
    class Meta:
        db_table = 'booking_ratings'
        verbose_name = '评价'
        verbose_name_plural = '评价'
    
    def __str__(self):
        return f"{self.booking} - {self.score}星"
