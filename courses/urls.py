from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('my/', views.MyCoursesView.as_view(), name='my_courses'),
    path('create/', views.course_create, name='course_create'),
    path('edit/<int:pk>/', views.course_edit, name='course_edit'),
    path('delete/<int:pk>/', views.course_delete, name='course_delete'),
    path('enroll/<int:pk>/', views.course_enroll, name='course_enroll'),
    path('enrollments/', views.my_enrollments, name='my_enrollments'),
    path('enrollment/cancel/<int:pk>/', views.enrollment_cancel, name='enrollment_cancel'),
    path('manage/enrollments/', views.EnrollmentManageView.as_view(), name='enrollment_manage'),
    path('manage/enrollments/confirm/<int:pk>/', views.enrollment_confirm, name='enrollment_confirm'),
]
