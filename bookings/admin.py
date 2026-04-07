from django.contrib import admin
from .models import Booking, BookingRating


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'space', 'booking_date', 'time_slot', 'status', 'created_at']
    list_filter = ['status', 'booking_date', 'created_at']
    search_fields = ['user__username', 'space__name']
    ordering = ['-created_at']
    list_per_page = 20
    list_select_related = ['user', 'space', 'space__venue']


@admin.register(BookingRating)
class BookingRatingAdmin(admin.ModelAdmin):
    list_display = ['booking', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['booking__user__username', 'booking__space__name']
    ordering = ['-created_at']
    list_per_page = 20
    list_select_related = ['booking', 'booking__user', 'booking__space']
