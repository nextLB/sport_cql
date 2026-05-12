from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # 教练
    path('coaches/', views.coach_list, name='coach_list'),
    path('coach/<int:coach_id>/', views.coach_detail, name='coach_detail'),
    path('coach/create/', views.coach_create, name='coach_create'),
    path('coach/edit/<int:coach_id>/', views.coach_edit, name='coach_edit'),
    path('coach/delete/<int:coach_id>/', views.coach_delete, name='coach_delete'),

    # 课程
    path('', views.course_list, name='course_list'),
    path('detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('create/', views.course_create, name='course_create'),
    path('edit/<int:course_id>/', views.course_edit, name='course_edit'),
    path('delete/<int:course_id>/', views.course_delete, name='course_delete'),

    # 报名
    path('enroll/<int:course_id>/', views.course_enroll, name='course_enroll'),
    path('cancel-enroll/<int:course_id>/', views.course_cancel_enroll, name='course_cancel_enroll'),
    path('my/', views.my_courses, name='my_courses'),
]
