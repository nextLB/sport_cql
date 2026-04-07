from django import forms
from .models import Booking, BookingRating
from venues.models import VenueSpace
from datetime import datetime, timedelta


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['space', 'booking_date', 'time_slot', 'contact_phone', 'remark']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['space'].widget.attrs['class'] = 'form-select'
        self.fields['booking_date'].widget.attrs['class'] = 'form-control'
        self.fields['time_slot'].widget.attrs['class'] = 'form-select'
        self.fields['contact_phone'].widget.attrs['class'] = 'form-control'
        self.fields['remark'].widget.attrs['class'] = 'form-control'
        self.fields['remark'].required = False


class BookingCreateForm(forms.Form):
    space_id = forms.IntegerField(widget=forms.HiddenInput())
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    time_slot = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    contact_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入联系电话'})
    )
    remark = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '请输入备注（可选）'})
    )
    
    def __init__(self, *args, **kwargs):
        space_id = kwargs.pop('space_id', None)
        super().__init__(*args, **kwargs)
        if space_id:
            try:
                space = VenueSpace.objects.get(pk=space_id)
                self.fields['space_id'].initial = space_id
                self.fields['contact_phone'].initial = ''
            except VenueSpace.DoesNotExist:
                pass


class BookingFilterForm(forms.Form):
    STATUS_CHOICES = [('', '全部状态')] + list(Booking.STATUS_CHOICES)
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label='预约状态',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    venue = forms.ModelChoiceField(
        queryset=VenueSpace.objects.all(),
        required=False,
        label='场地',
        empty_label='全部场地',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        label='开始日期',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        label='结束日期',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )


class BookingRatingForm(forms.ModelForm):
    class Meta:
        model = BookingRating
        fields = ['score', 'comment']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].widget.attrs['class'] = 'form-select'
        self.fields['comment'].widget.attrs['class'] = 'form-control'
        self.fields['comment'].required = False
