from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from venues.models import Venue
from bookings.models import Booking
from users.models import User


def home(request):
    venues = Venue.objects.filter(status='open').order_by('-created_at')[:6]
    return render(request, 'home.html', {
        'venues': venues
    })


@login_required
def dashboard(request):
    if request.user.user_type == 'admin' or request.user.is_staff:
        return admin_dashboard(request)
    return user_dashboard(request)


def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'dashboard/user_dashboard.html', {
        'bookings': bookings
    })


@login_required
def admin_dashboard(request):
    total_venues = Venue.objects.count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    total_users = User.objects.filter(user_type='user').count()
    recent_bookings = Booking.objects.select_related('user', 'field__venue').order_by('-created_at')[:10]
    
    return render(request, 'dashboard/admin_dashboard.html', {
        'total_venues': total_venues,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'total_users': total_users,
        'recent_bookings': recent_bookings
    })
