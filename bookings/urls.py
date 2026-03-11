from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:field_id>/', views.booking_create, name='booking_create'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('cancel/<int:booking_id>/', views.booking_cancel, name='booking_cancel'),
    path('manage/', views.booking_manage, name='booking_manage'),
    path('approve/<int:booking_id>/', views.booking_approve, name='booking_approve'),
    path('edit/<int:booking_id>/', views.booking_edit, name='booking_edit'),
    path('delete/<int:booking_id>/', views.booking_delete, name='booking_delete'),
    path('review/<int:booking_id>/', views.booking_review, name='booking_review'),
]
