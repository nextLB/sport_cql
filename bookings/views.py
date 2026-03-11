from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Booking, BookingReview
from .forms import BookingForm, BookingReviewForm
from venues.models import Field


@login_required
def booking_create(request, field_id):
    field = get_object_or_404(Field, id=field_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.field = field
            
            hours = (booking.end_time.hour - booking.start_time.hour) + (booking.end_time.minute - booking.start_time.minute) / 60
            booking.total_price = field.venue.price_per_hour * hours
            
            if not check_field_available(field, booking.booking_date, 
                                         booking.start_time, booking.end_time):
                messages.error(request, '该时间段已被预约')
                return render(request, 'bookings/booking_form.html', {
                    'form': form,
                    'field': field
                })
            
            booking.save()
            messages.success(request, '预约成功！请等待审批')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    
    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'field': field
    })


def check_field_available(field, date, start_time, end_time):
    conflicting = Booking.objects.filter(
        field=field,
        booking_date=date,
        status__in=['pending', 'confirmed'],
        start_time__lt=end_time,
        end_time__gt=start_time
    )
    return not conflicting.exists()


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('field__venue')
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookings/my_bookings.html', {
        'page_obj': page_obj,
        'status': status
    })


@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, '预约已取消')
    else:
        messages.error(request, '该预约无法取消')
    return redirect('my_bookings')


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking
    })


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def booking_manage(request):
    bookings = Booking.objects.select_related('user', 'field__venue')
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookings/booking_manage.html', {
        'page_obj': page_obj,
        'status': status
    })


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def booking_approve(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    action = request.POST.get('action')
    
    if action == 'confirm':
        booking.status = 'confirmed'
        messages.success(request, f'预约 {booking.id} 已确认')
    elif action == 'reject':
        booking.status = 'rejected'
        messages.success(request, f'预约 {booking.id} 已拒绝')
    
    booking.save()
    return redirect('booking_manage')


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def booking_edit(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, '预约更新成功')
            return redirect('booking_manage')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'booking': booking
    })


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    messages.success(request, '预约已删除')
    return redirect('booking_manage')


@login_required
def booking_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'completed':
        messages.error(request, '只能评价已完成的预约')
        return redirect('my_bookings')
    
    if hasattr(booking, 'review'):
        messages.error(request, '该预约已评价')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        form = BookingReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, '评价成功')
            return redirect('my_bookings')
    else:
        form = BookingReviewForm()
    
    return render(request, 'bookings/review_form.html', {
        'form': form,
        'booking': booking
    })
