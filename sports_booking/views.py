from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from venues.models import Venue
from bookings.models import Booking
from users.models import User
from django.db.models import Sum, Count, Avg


def home(request):
    venues = Venue.objects.filter(status='open').order_by('-created_at')[:6]
    from venues.models import Field
    from bookings.models import Booking
    from users.models import User
    
    total_venues = Venue.objects.count()
    total_fields = Field.objects.count()
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()
    
    return render(request, 'home.html', {
        'venues': venues,
        'total_venues': total_venues,
        'total_fields': total_fields,
        'total_bookings': total_bookings,
        'total_users': total_users
    })


@login_required
def dashboard(request):
    if request.user.user_type == 'admin' or request.user.is_staff:
        return admin_dashboard(request)
    elif request.user.user_type == 'coach':
        return coach_dashboard(request)
    return user_dashboard(request)


def coach_dashboard(request):
    from courses.models import Course, CourseEnrollment
    my_courses = Course.objects.filter(coach__phone=request.user.phone).order_by('-created_at')
    # 如果教练还没有关联的Coach记录，则通过用户名匹配
    if not my_courses.exists():
        from courses.models import Coach
        try:
            coach = Coach.objects.get(name=request.user.username)
            my_courses = Course.objects.filter(coach=coach).order_by('-created_at')
        except Coach.DoesNotExist:
            my_courses = Course.objects.none()

    pending_enrollments = CourseEnrollment.objects.filter(
        course__in=my_courses, status='enrolled'
    ).count()

    return render(request, 'dashboard/coach_dashboard.html', {
        'my_courses': my_courses,
        'course_count': my_courses.count(),
        'pending_enrollments': pending_enrollments
    })


def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'dashboard/user_dashboard.html', {
        'bookings': bookings
    })


@login_required
def admin_dashboard(request):
    from django.db.models import Q
    
    total_venues = Venue.objects.count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    total_users = User.objects.filter(user_type='user').count()
    recent_bookings = Booking.objects.select_related('user', 'field__venue').order_by('-created_at')[:10]
    
    total_revenue = Booking.objects.filter(
        status__in=['confirmed', 'completed']
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0

    venue_stats = {
        'open': Venue.objects.filter(status='open').count(),
        'closed': Venue.objects.filter(status='closed').count(),
        'maintenance': Venue.objects.filter(status='maintenance').count(),
    }

    from bookings.models import BookingReview
    total_reviews = BookingReview.objects.count()
    recent_reviews = BookingReview.objects.select_related('booking__user', 'booking__field__venue').order_by('-created_at')[:5]
    avg_rating = BookingReview.objects.aggregate(avg=Avg('rating'))['avg'] or 0

    return render(request, 'dashboard/admin_dashboard.html', {
        'total_venues': total_venues,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'venue_stats': venue_stats,
        'total_reviews': total_reviews,
        'recent_reviews': recent_reviews,
        'avg_rating': avg_rating
    })
