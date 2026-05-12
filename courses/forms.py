from django import forms
from .models import Coach, Course


class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['name', 'gender', 'phone', 'email', 'avatar',
                  'speciality', 'description', 'experience', 'certificate', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '教练姓名'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '联系电话'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '邮箱（可选）'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'speciality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '多个项目用逗号分隔，如：篮球,足球,游泳'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '个人简介'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'certificate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '如：国家一级教练员'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'coach', 'venue', 'course_type', 'description',
                  'max_students', 'price', 'start_date', 'end_date', 'schedule', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '课程名称'}),
            'coach': forms.Select(attrs={'class': 'form-control'}),
            'venue': forms.Select(attrs={'class': 'form-control'}),
            'course_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '课程描述'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'schedule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '如：每周一、三、五 18:00-20:00'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
