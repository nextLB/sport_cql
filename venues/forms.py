from django import forms
from .models import Venue, VenueSpace


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'venue_type', 'address', 'description', 'opening_hours', 'phone', 'image', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'description':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
            elif field_name == 'image':
                field.widget.attrs['class'] = 'form-control-file'


class VenueSpaceForm(forms.ModelForm):
    class Meta:
        model = VenueSpace
        fields = ['venue', 'name', 'space_type', 'capacity', 'price', 'description', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'description':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            elif field_name == 'venue':
                field.widget.attrs['class'] = 'form-select'
            elif field_name == 'status':
                field.widget.attrs['class'] = 'form-select'
            elif field_name == 'space_type':
                field.widget.attrs['class'] = 'form-select'


class VenueSpaceFilterForm(forms.Form):
    venue = forms.ModelChoiceField(
        queryset=Venue.objects.all(),
        required=False,
        label='所属场馆',
        empty_label='全部场馆',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', '全部状态')] + list(VenueSpace.STATUS_CHOICES),
        required=False,
        label='场地状态',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
