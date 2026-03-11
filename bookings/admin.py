from django.contrib import admin
from .models import Booking, BookingReview


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'field', 'booking_date', 'start_time', 'end_time', 'status', 'total_price', 'contact_phone', 'created_at']
    list_filter = ['status', 'booking_date', 'created_at', 'field__venue']
    search_fields = ['user__username', 'field__name', 'contact_phone']
    ordering = ['-created_at']
    list_editable = ['status']
    date_hierarchy = 'booking_date'


@admin.register(BookingReview)
class BookingReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['booking__user__username', 'comment']
    ordering = ['-created_at']
