from django.urls import path
from . import views

app_name = 'venues'

urlpatterns = [
    path('', views.venue_list, name='venue_list'),
    path('detail/<int:venue_id>/', views.venue_detail, name='venue_detail'),
    path('fields/', views.field_list, name='field_list'),
    path('field/<int:field_id>/', views.field_detail, name='field_detail'),
    path('create/', views.venue_create, name='venue_create'),
    path('edit/<int:venue_id>/', views.venue_edit, name='venue_edit'),
    path('delete/<int:venue_id>/', views.venue_delete, name='venue_delete'),
    path('field/create/', views.field_create, name='field_create'),
    path('field/edit/<int:field_id>/', views.field_edit, name='field_edit'),
    path('field/delete/<int:field_id>/', views.field_delete, name='field_delete'),
    path('field/<int:field_id>/schedule/', views.get_field_schedule, name='field_schedule'),
]
