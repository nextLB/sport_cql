from django import forms
from .models import Course, CourseEnrollment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'sport_type', 'venue_space', 'description', 'price', 
                  'max_participants', 'start_date', 'end_date', 'start_time', 'end_time', 'recurring_days']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['description']:
                field.widget.attrs['rows'] = '4'


class CourseFilterForm(forms.Form):
    sport_type = forms.ChoiceField(
        label='运动类型',
        choices=[('', '全部')] + list(Course.SPORT_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        label='状态',
        choices=[('', '全部')] + list(Course.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    keyword = forms.CharField(
        label='关键词',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '课程名称'})
    )


class CourseEnrollmentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EnrollmentConfirmForm(forms.Form):
    status = forms.ChoiceField(
        label='审批结果',
        choices=[('confirmed', '确认'), ('cancelled', '拒绝')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
