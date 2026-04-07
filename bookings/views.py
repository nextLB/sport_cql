from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, View
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
from .models import Booking, BookingRating
from .forms import BookingCreateForm, BookingFilterForm, BookingRatingForm
from venues.models import VenueSpace


class MyBookingsView(ListView):
    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = BookingFilterForm(self.request.GET)
        status = self.request.GET.get('status')
        if status:
            context['bookings'] = context['bookings'].filter(status=status)
        return context


@login_required
def booking_create(request):
    space_id = request.GET.get('space_id')
    if not space_id:
        messages.error(request, '请选择要预约的场地。')
        return redirect('venues:venue_list')
    
    space = get_object_or_404(VenueSpace, pk=space_id)
    
    if request.method == 'POST':
        form = BookingCreateForm(request.POST, space_id=space_id)
        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            time_slot = form.cleaned_data['time_slot']
            
            if booking_date < datetime.now().date():
                messages.error(request, '不能预约过去的时间。')
                return render(request, 'bookings/booking_form.html', {'form': form, 'space': space})
            
            if Booking.objects.filter(
                space=space,
                booking_date=booking_date,
                time_slot=time_slot,
                status__in=['pending', 'confirmed']
            ).exists():
                messages.error(request, '该时段已被预约，请选择其他时间段。')
                return render(request, 'bookings/booking_form.html', {'form': form, 'space': space})
            
            booking = Booking(
                user=request.user,
                space=space,
                booking_date=booking_date,
                time_slot=time_slot,
                contact_phone=form.cleaned_data['contact_phone'],
                remark=form.cleaned_data.get('remark', ''),
                status='pending'
            )
            booking.save()
            messages.success(request, '预约提交成功！请等待审批。')
            return redirect('bookings:my_bookings')
    else:
        form = BookingCreateForm(space_id=space_id)
    
    return render(request, 'bookings/booking_form.html', {'form': form, 'space': space})


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if not booking.can_cancel:
        messages.error(request, '该状态无法取消预约。')
        return redirect('bookings:my_bookings')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, '预约取消成功！')
        return redirect('bookings:my_bookings')
    
    return render(request, 'bookings/booking_cancel.html', {'booking': booking})


@login_required
def booking_rate(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if not booking.can_rate:
        messages.error(request, '该预约无法评价。')
        return redirect('bookings:my_bookings')
    
    if request.method == 'POST':
        form = BookingRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.booking = booking
            rating.save()
            messages.success(request, '评价提交成功！感谢您的反馈。')
            return redirect('bookings:my_bookings')
    else:
        form = BookingRatingForm()
    
    return render(request, 'bookings/booking_rate.html', {'form': form, 'booking': booking})


class BookingManageView(ListView):
    model = Booking
    template_name = 'bookings/booking_manage.html'
    context_object_name = 'bookings'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Booking.objects.all()
        
        status = self.request.GET.get('status')
        venue_id = self.request.GET.get('venue')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if status:
            queryset = queryset.filter(status=status)
        if venue_id:
            queryset = queryset.filter(space__venue_id=venue_id)
        if date_from:
            queryset = queryset.filter(booking_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(booking_date__lte=date_to)
        
        return queryset.select_related('user', 'space', 'space__venue')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from venues.models import Venue
        context['venues'] = Venue.objects.all()
        context['filter_form'] = BookingFilterForm(self.request.GET)
        return context


@login_required
def booking_confirm(request, pk):
    if not request.user.is_staff:
        messages.error(request, '您没有权限执行此操作。')
        return redirect('home')
    
    booking = get_object_or_404(Booking, pk=pk, status='pending')
    
    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, '预约已确认！')
        return redirect('bookings:booking_manage')
    
    return render(request, 'bookings/booking_confirm.html', {'booking': booking})


@login_required
def booking_reject(request, pk):
    if not request.user.is_staff:
        messages.error(request, '您没有权限执行此操作。')
        return redirect('home')
    
    booking = get_object_or_404(Booking, pk=pk, status='pending')
    
    if request.method == 'POST':
        reject_reason = request.POST.get('reject_reason', '')
        booking.status = 'rejected'
        booking.reject_reason = reject_reason
        booking.save()
        messages.success(request, '预约已拒绝！')
        return redirect('bookings:booking_manage')
    
    return render(request, 'bookings/booking_reject.html', {'booking': booking})


@login_required
def booking_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, '您没有权限执行此操作。')
        return redirect('home')
    
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        new_date = request.POST.get('booking_date')
        new_time = request.POST.get('time_slot')
        new_phone = request.POST.get('contact_phone')
        
        if new_date and new_time:
            conflict = Booking.objects.filter(
                space=booking.space,
                booking_date=new_date,
                time_slot=new_time,
                status__in=['pending', 'confirmed']
            ).exclude(pk=pk).exists()
            
            if conflict:
                messages.error(request, '该时段已被占用，无法修改。')
            else:
                booking.booking_date = new_date
                booking.time_slot = new_time
                booking.contact_phone = new_phone
                booking.save()
                messages.success(request, '预约信息更新成功！')
                return redirect('bookings:booking_manage')
    
    return render(request, 'bookings/booking_edit.html', {'booking': booking})


@login_required
def booking_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, '您没有权限执行此操作。')
        return redirect('home')
    
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, '预约删除成功！')
        return redirect('bookings:booking_manage')
    
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})
