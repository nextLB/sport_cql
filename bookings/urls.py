from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('my/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('create/', views.booking_create, name='booking_create'),
    path('cancel/<int:pk>/', views.booking_cancel, name='booking_cancel'),
    path('rate/<int:pk>/', views.booking_rate, name='booking_rate'),
    path('manage/', views.BookingManageView.as_view(), name='booking_manage'),
    path('confirm/<int:pk>/', views.booking_confirm, name='booking_confirm'),
    path('reject/<int:pk>/', views.booking_reject, name='booking_reject'),
    path('edit/<int:pk>/', views.booking_edit, name='booking_edit'),
    path('delete/<int:pk>/', views.booking_delete, name='booking_delete'),
]
