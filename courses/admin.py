from django.contrib import admin
from .models import Course, CourseEnrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'coach', 'sport_type', 'start_date', 'status', 'current_participants', 'max_participants']
    list_filter = ['sport_type', 'status']
    search_fields = ['course_name', 'coach__username']
    raw_id_fields = ['coach', 'venue_space']


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'status', 'created_at']
    list_filter = ['status']
    raw_id_fields = ['course', 'user']
