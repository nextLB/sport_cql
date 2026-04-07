from django.urls import path
from . import views

app_name = 'venues'

urlpatterns = [
    path('', views.VenueListView.as_view(), name='venue_list'),
    path('detail/<int:pk>/', views.VenueDetailView.as_view(), name='venue_detail'),
    path('create/', views.venue_create, name='venue_create'),
    path('edit/<int:pk>/', views.venue_edit, name='venue_edit'),
    path('delete/<int:pk>/', views.venue_delete, name='venue_delete'),
    path('spaces/', views.VenueSpaceListView.as_view(), name='space_list'),
    path('spaces/create/', views.venue_space_create, name='space_create'),
    path('spaces/edit/<int:pk>/', views.venue_space_edit, name='space_edit'),
    path('spaces/delete/<int:pk>/', views.venue_space_delete, name='space_delete'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),
]
