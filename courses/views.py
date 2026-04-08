from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
from .models import Course, CourseEnrollment
from .forms import CourseForm, CourseFilterForm, EnrollmentConfirmForm
from venues.models import VenueSpace


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Course.objects.filter(status__in=['open', 'full', 'ongoing'])
        sport_type = self.request.GET.get('sport_type')
        keyword = self.request.GET.get('keyword')
        
        if sport_type:
            queryset = queryset.filter(sport_type=sport_type)
        if keyword:
            queryset = queryset.filter(course_name__icontains=keyword)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sport_types'] = Course.SPORT_CHOICES
        context['filter_form'] = CourseFilterForm(self.request.GET)
        return context


class MyCoursesView(ListView):
    model = Course
    template_name = 'courses/my_courses.html'
    context_object_name = 'courses'
    paginate_by = 10
    
    def get_queryset(self):
        return Course.objects.filter(coach=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CourseFilterForm(self.request.GET)
        return context


@login_required
def course_create(request):
    if request.user.role != 'coach' and not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('home')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.coach = request.user
            course.save()
            messages.success(request, '课程创建成功！')
            return redirect('courses:my_courses')
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_form.html', {'form': form, 'action': '创建'})


@login_required
def course_edit(request, pk):
    if request.user.role != 'coach' and not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('home')
    
    course = get_object_or_404(Course, pk=pk, coach=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, '课程更新成功！')
            return redirect('courses:my_courses')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_form.html', {'form': form, 'action': '编辑'})


@login_required
def course_delete(request, pk):
    if request.user.role != 'coach' and not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('home')
    
    course = get_object_or_404(Course, pk=pk, coach=request.user)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, '课程删除成功！')
        return redirect('courses:my_courses')
    
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@login_required
def course_enroll(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if course.coach == request.user:
        messages.error(request, '您不能报名自己的课程。')
        return redirect('courses:course_list')
    
    if CourseEnrollment.objects.filter(course=course, user=request.user).exists():
        messages.error(request, '您已报名过该课程。')
        return redirect('courses:course_list')
    
    if course.is_full:
        messages.error(request, '该课程已满员。')
        return redirect('courses:course_list')
    
    enrollment = CourseEnrollment(course=course, user=request.user, status='pending')
    enrollment.save()
    messages.success(request, '报名成功！请等待教练审批。')
    return redirect('courses:course_list')


class EnrollmentManageView(ListView):
    model = CourseEnrollment
    template_name = 'courses/enrollment_manage.html'
    context_object_name = 'enrollments'
    paginate_by = 20
    
    def get_queryset(self):
        course_id = self.request.GET.get('course')
        status = self.request.GET.get('status')
        
        queryset = CourseEnrollment.objects.filter(course__coach=self.request.user)
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.select_related('course', 'user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(coach=self.request.user)
        return context


@login_required
def enrollment_confirm(request, pk):
    enrollment = get_object_or_404(CourseEnrollment, pk=pk, course__coach=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('status')
        if action == 'confirmed':
            enrollment.status = 'confirmed'
            enrollment.course.current_participants += 1
            enrollment.course.save()
            messages.success(request, '已确认该学员报名！')
        elif action == 'cancelled':
            enrollment.status = 'cancelled'
            enrollment.save()
            messages.success(request, '已拒绝该学员报名。')
        return redirect('courses:enrollment_manage')
    
    return render(request, 'courses/enrollment_confirm.html', {'enrollment': enrollment})


@login_required
def my_enrollments(request):
    enrollments = CourseEnrollment.objects.filter(user=request.user).select_related('course', 'course__coach')
    status = request.GET.get('status')
    if status:
        enrollments = enrollments.filter(status=status)
    return render(request, 'courses/my_enrollments.html', {'enrollments': enrollments})


@login_required
def enrollment_cancel(request, pk):
    enrollment = get_object_or_404(CourseEnrollment, pk=pk, user=request.user)
    
    if enrollment.status not in ['pending', 'confirmed']:
        messages.error(request, '该状态无法取消。')
        return redirect('courses:my_enrollments')
    
    if request.method == 'POST':
        enrollment.status = 'cancelled'
        enrollment.save()
        
        if enrollment.status == 'confirmed':
            enrollment.course.current_participants -= 1
            enrollment.course.save()
        
        messages.success(request, '已取消报名。')
        return redirect('courses:my_enrollments')
    
    return render(request, 'courses/enrollment_cancel.html', {'enrollment': enrollment})
