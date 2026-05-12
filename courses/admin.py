from django.contrib import admin
from .models import Coach, Course, CourseEnrollment


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'phone', 'speciality', 'experience', 'status', 'created_at']
    list_filter = ['gender', 'status', 'created_at']
    search_fields = ['name', 'phone', 'speciality', 'description']
    ordering = ['-created_at']
    list_editable = ['status']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'coach', 'venue', 'course_type', 'max_students', 'price', 'start_date', 'end_date', 'status', 'enrolled_count']
    list_filter = ['course_type', 'status', 'start_date', 'coach', 'venue']
    search_fields = ['name', 'coach__name', 'venue__name', 'description']
    ordering = ['-created_at']
    list_editable = ['status']
    date_hierarchy = 'start_date'


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'course']
    search_fields = ['course__name', 'user__username']
    ordering = ['-created_at']
    list_editable = ['status']
