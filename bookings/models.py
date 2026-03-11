from django.db import models
from django.conf import settings
from venues.models import Field


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审批'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
        ('rejected', '已拒绝'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', verbose_name='预约用户')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='bookings', verbose_name='预约场地')
    booking_date = models.DateField(verbose_name='预约日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='预约状态')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'bookings'
        verbose_name = '预约'
        verbose_name_plural = '预约'
        ordering = ['-booking_date', '-start_time']

    def __str__(self):
        return f"{self.user.username} - {self.field.name} - {self.booking_date}"

    @property
    def hours(self):
        from datetime import datetime
        start = datetime.combine(self.booking_date, self.start_time)
        end = datetime.combine(self.booking_date, self.end_time)
        return (end - start).seconds / 3600


class BookingReview(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review', verbose_name='预约')
    rating = models.IntegerField(verbose_name='评分', choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, verbose_name='评价内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评价时间')

    class Meta:
        db_table = 'booking_reviews'
        verbose_name = '预约评价'
        verbose_name_plural = '预约评价'

    def __str__(self):
        return f"评价 - {self.booking.id}"
