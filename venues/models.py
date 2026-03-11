from django.db import models


class Venue(models.Model):
    VENUE_TYPE_CHOICES = (
        ('football', '足球场'),
        ('basketball', '篮球场'),
        ('tennis', '网球场'),
        ('badminton', '羽毛球场'),
        ('swimming', '游泳池'),
        ('table_tennis', '乒乓球室'),
        ('fitness', '健身房'),
        ('other', '其他'),
    )
    
    STATUS_CHOICES = (
        ('open', '开放'),
        ('closed', '关闭'),
        ('maintenance', '维护中'),
    )
    
    name = models.CharField(max_length=100, verbose_name='场馆名称')
    venue_type = models.CharField(max_length=20, choices=VENUE_TYPE_CHOICES, verbose_name='场馆类型')
    address = models.TextField(verbose_name='地址')
    description = models.TextField(blank=True, verbose_name='描述')
    image = models.ImageField(upload_to='venues/', blank=True, verbose_name='场馆图片')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    opening_hours = models.CharField(max_length=100, verbose_name='营业时间')
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='每小时价格')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'venues'
        verbose_name = '场馆'
        verbose_name_plural = '场馆'

    def __str__(self):
        return self.name


class Field(models.Model):
    FIELD_TYPE_CHOICES = (
        ('indoor', '室内'),
        ('outdoor', '室外'),
    )
    
    STATUS_CHOICES = (
        ('available', '可用'),
        ('occupied', '已占用'),
        ('maintenance', '维护中'),
        ('disabled', '不可用'),
    )
    
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='fields', verbose_name='所属场馆')
    name = models.CharField(max_length=50, verbose_name='场地名称')
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES, verbose_name='场地类型')
    capacity = models.IntegerField(verbose_name='容纳人数')
    description = models.TextField(blank=True, verbose_name='描述')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'fields'
        verbose_name = '场地'
        verbose_name_plural = '场地'

    def __str__(self):
        return f"{self.venue.name} - {self.name}"
