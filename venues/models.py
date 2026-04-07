from django.db import models


class Venue(models.Model):
    STATUS_CHOICES = [
        ('open', '开放'),
        ('closed', '关闭'),
        ('maintenance', '维护中'),
    ]
    
    TYPE_CHOICES = [
        ('basketball', '篮球馆'),
        ('badminton', '羽毛球馆'),
        ('tennis', '网球馆'),
        ('football', '足球场'),
        ('swimming', '游泳池'),
        ('fitness', '健身房'),
        ('other', '其他'),
    ]
    
    name = models.CharField('场馆名称', max_length=100, unique=True)
    venue_type = models.CharField('场馆类型', max_length=20, choices=TYPE_CHOICES, default='other')
    address = models.CharField('地址', max_length=200)
    description = models.TextField('详细介绍', blank=True)
    opening_hours = models.CharField('营业时间', max_length=100, default='09:00-22:00')
    phone = models.CharField('联系电话', max_length=20)
    image = models.ImageField('场馆图片', upload_to='venues/', null=True, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'venues'
        verbose_name = '场馆'
        verbose_name_plural = '场馆'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_venue_type_display(self):
        return dict(self.TYPE_CHOICES).get(self.venue_type, '其他')
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, '未知')
    
    @property
    def venue_count(self):
        return self.venue_spaces.count()
    
    @property
    def available_count(self):
        return self.venue_spaces.filter(status='available').count()


class VenueSpace(models.Model):
    STATUS_CHOICES = [
        ('available', '可用'),
        ('maintenance', '维护中'),
        ('occupied', '占用'),
        ('unavailable', '不可用'),
    ]
    
    TYPE_CHOICES = [
        ('indoor', '室内'),
        ('outdoor', '室外'),
    ]
    
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='venue_spaces', verbose_name='所属场馆')
    name = models.CharField('场地名称', max_length=100)
    space_type = models.CharField('场地类型', max_length=20, choices=TYPE_CHOICES, default='indoor')
    capacity = models.IntegerField('容纳人数', default=1)
    price = models.DecimalField('价格(元/小时)', max_digits=10, decimal_places=2)
    description = models.TextField('场地描述', blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'venue_spaces'
        verbose_name = '场地'
        verbose_name_plural = '场地'
        ordering = ['-created_at']
        unique_together = ['venue', 'name']
    
    def __str__(self):
        return f"{self.venue.name} - {self.name}"
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, '未知')
