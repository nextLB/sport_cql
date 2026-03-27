from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Venue, Field
from .forms import VenueForm, FieldForm


def venue_list(request):
    venues = Venue.objects.filter(status='open').order_by('-created_at')
    venue_type = request.GET.get('type')
    if venue_type:
        venues = venues.filter(venue_type=venue_type)
    
    search = request.GET.get('search')
    if search:
        venues = venues.filter(name__icontains=search)
    
    paginator = Paginator(venues, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'venues/venue_list.html', {
        'page_obj': page_obj,
        'venue_type': venue_type,
        'search': search
    })


def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    fields = venue.fields.all()
    return render(request, 'venues/venue_detail.html', {
        'venue': venue,
        'fields': fields
    })


def field_list(request):
    fields = Field.objects.select_related('venue').filter(status='available')
    venue_id = request.GET.get('venue')
    if venue_id:
        fields = fields.filter(venue_id=venue_id)
    
    paginator = Paginator(fields, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'venues/field_list.html', {
        'page_obj': page_obj
    })


def field_detail(request, field_id):
    field = get_object_or_404(Field.objects.select_related('venue'), id=field_id)
    return render(request, 'venues/field_detail.html', {
        'field': field
    })


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def venue_create(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '场馆创建成功')
            return redirect('venues:venue_list')
    else:
        form = VenueForm()
    return render(request, 'venues/venue_form.html', {'form': form})


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def venue_edit(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            messages.success(request, '场馆更新成功')
            return redirect('venues:venue_list')
    else:
        form = VenueForm(instance=venue)
    return render(request, 'venues/venue_form.html', {'form': form})


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def venue_delete(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    venue.delete()
    messages.success(request, '场馆删除成功')
    return redirect('venues:venue_list')


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def field_create(request):
    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '场地创建成功')
            return redirect('venues:field_list')
    else:
        form = FieldForm()
    return render(request, 'venues/field_form.html', {'form': form})


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def field_edit(request, field_id):
    field = get_object_or_404(Field, id=field_id)
    if request.method == 'POST':
        form = FieldForm(request.POST, instance=field)
        if form.is_valid():
            form.save()
            messages.success(request, '场地更新成功')
            return redirect('venues:field_list')
    else:
        form = FieldForm(instance=field)
    return render(request, 'venues/field_form.html', {'form': form})


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def field_delete(request, field_id):
    field = get_object_or_404(Field, id=field_id)
    field.delete()
    messages.success(request, '场地删除成功')
    return redirect('venues:field_list')


def get_field_schedule(request, field_id):
    from datetime import datetime, timedelta
    from bookings.models import Booking
    
    field = get_object_or_404(Field, id=field_id)
    date_str = request.GET.get('date')
    
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = datetime.now().date()
    else:
        date = datetime.now().date()
    
    bookings = Booking.objects.filter(
        field=field,
        booking_date=date,
        status__in=['pending', 'confirmed']
    )
    
    booked_slots = []
    for booking in bookings:
        booked_slots.append({
            'start': booking.start_time.strftime('%H:%M'),
            'end': booking.end_time.strftime('%H:%M')
        })
    
    return JsonResponse({
        'field': {
            'id': field.id,
            'name': field.name,
            'venue': field.venue.name,
            'price_per_hour': float(field.venue.price_per_hour)
        },
        'date': date.strftime('%Y-%m-%d'),
        'booked_slots': booked_slots
    })
