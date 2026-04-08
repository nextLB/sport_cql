from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', '普通用户'),
        ('coach', '教练'),
        ('admin', '管理员'),
    ]
    
    STATUS_CHOICES = [
        ('active', '启用'),
        ('disabled', '禁用'),
    ]
    
    email = models.EmailField('邮箱', unique=True, null=True, blank=True)
    phone = models.CharField('手机号', max_length=20, null=True, blank=True)
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='user')
    status = models.CharField('账户状态', max_length=20, choices=STATUS_CHOICES, default='active')
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
