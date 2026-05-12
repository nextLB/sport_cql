from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Coach, Course, CourseEnrollment
from .forms import CoachForm, CourseForm


# ==================== 教练视图 ====================

def coach_list(request):
    coaches = Coach.objects.filter(status='active').order_by('-created_at')
    speciality = request.GET.get('speciality')
    search = request.GET.get('search')

    if speciality:
        coaches = coaches.filter(speciality__icontains=speciality)
    if search:
        coaches = coaches.filter(name__icontains=search)

    paginator = Paginator(coaches, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/coach_list.html', {
        'page_obj': page_obj,
        'speciality': speciality,
        'search': search
    })


def coach_detail(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)
    courses = coach.courses.all().order_by('-start_date')
    return render(request, 'courses/coach_detail.html', {
        'coach': coach,
        'courses': courses
    })


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def coach_create(request):
    if request.method == 'POST':
        form = CoachForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '教练添加成功')
            return redirect('courses:coach_list')
    else:
        form = CoachForm()
    return render(request, 'courses/coach_form.html', {'form': form})


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def coach_edit(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)
    if request.method == 'POST':
        form = CoachForm(request.POST, request.FILES, instance=coach)
        if form.is_valid():
            form.save()
            messages.success(request, '教练信息更新成功')
            return redirect('courses:coach_list')
    else:
        form = CoachForm(instance=coach)
    return render(request, 'courses/coach_form.html', {'form': form})


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def coach_delete(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)
    coach.delete()
    messages.success(request, '教练已删除')
    return redirect('courses:coach_list')


# ==================== 课程视图 ====================

def course_list(request):
    courses = Course.objects.select_related('coach', 'venue').order_by('-created_at')

    course_type = request.GET.get('type')
    coach_id = request.GET.get('coach')
    status = request.GET.get('status')
    search = request.GET.get('search')

    if course_type:
        courses = courses.filter(course_type=course_type)
    if coach_id:
        courses = courses.filter(coach_id=coach_id)
    if status:
        courses = courses.filter(status=status)
    if search:
        courses = courses.filter(name__icontains=search)

    coaches = Coach.objects.filter(status='active')

    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/course_list.html', {
        'page_obj': page_obj,
        'coaches': coaches,
        'current_type': course_type,
        'current_coach': coach_id,
        'current_status': status,
        'search': search
    })


def course_detail(request, course_id):
    course = get_object_or_404(Course.objects.select_related('coach', 'venue'), id=course_id)
    enrollments = course.enrollments.filter(status='enrolled').select_related('user')
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = course.enrollments.filter(user=request.user, status='enrolled').exists()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'enrollments': enrollments,
        'is_enrolled': is_enrolled
    })


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '课程创建成功')
            return redirect('courses:course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, '课程更新成功')
            return redirect('courses:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, '课程已删除')
    return redirect('courses:course_list')


# ==================== 报名视图 ====================

@login_required
def course_enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if course.status != 'enrolling':
        messages.error(request, '该课程当前不在报名阶段')
        return redirect('courses:course_detail', course_id=course.id)

    if course.enrolled_count >= course.max_students:
        messages.error(request, '该课程已满员')
        return redirect('courses:course_detail', course_id=course.id)

    enrollment, created = CourseEnrollment.objects.get_or_create(
        course=course,
        user=request.user,
        defaults={'status': 'enrolled'}
    )

    if created:
        messages.success(request, f'成功报名课程：{course.name}')
    else:
        if enrollment.status == 'cancelled':
            enrollment.status = 'enrolled'
            enrollment.save()
            messages.success(request, f'重新报名成功：{course.name}')
        else:
            messages.info(request, '您已报名该课程')

    return redirect('courses:course_detail', course_id=course.id)


@login_required
def course_cancel_enroll(request, course_id):
    enrollment = get_object_or_404(CourseEnrollment, course_id=course_id, user=request.user)

    if enrollment.status == 'enrolled':
        enrollment.status = 'cancelled'
        enrollment.save()
        messages.success(request, '已取消报名')
    else:
        messages.error(request, '无法取消该报名')

    return redirect('courses:course_detail', course_id=course_id)


@login_required
def my_courses(request):
    enrollments = CourseEnrollment.objects.filter(
        user=request.user
    ).select_related('course__coach', 'course__venue').order_by('-created_at')

    paginator = Paginator(enrollments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/my_courses.html', {
        'page_obj': page_obj
    })
