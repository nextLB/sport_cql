from django.contrib import admin
from .models import Venue, Field


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue_type', 'address', 'price_per_hour', 'status', 'created_at']
    list_filter = ['venue_type', 'status', 'created_at']
    search_fields = ['name', 'address', 'description']
    ordering = ['-created_at']
    list_editable = ['status']


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'field_type', 'capacity', 'status', 'created_at']
    list_filter = ['field_type', 'status', 'venue__venue_type']
    search_fields = ['name', 'venue__name', 'description']
    ordering = ['-created_at']
    list_editable = ['status']
