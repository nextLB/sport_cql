from django import forms
from .models import Venue, Field


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'venue_type', 'address', 'description', 'image', 
                  'phone', 'opening_hours', 'price_per_hour', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'venue_type': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'opening_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例如: 08:00-22:00'}),
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['venue', 'name', 'field_type', 'capacity', 'description', 'status']
        widgets = {
            'venue': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'field_type': forms.Select(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
