from django.contrib import admin
from .models import Venue, VenueSpace


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue_type', 'address', 'phone', 'status', 'created_at']
    list_filter = ['venue_type', 'status', 'created_at']
    search_fields = ['name', 'address', 'phone']
    ordering = ['-created_at']
    list_per_page = 20


@admin.register(VenueSpace)
class VenueSpaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'space_type', 'capacity', 'price', 'status', 'created_at']
    list_filter = ['venue', 'space_type', 'status', 'created_at']
    search_fields = ['name', 'venue__name']
    ordering = ['-created_at']
    list_per_page = 20
    list_select_related = ['venue']
