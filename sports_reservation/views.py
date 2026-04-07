from django.shortcuts import render
from django.views.generic import TemplateView
from venues.models import Venue, VenueSpace
from bookings.models import Booking


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['venues'] = Venue.objects.filter(status='open')[:6]
        context['venue_count'] = Venue.objects.filter(status='open').count()
        context['space_count'] = VenueSpace.objects.filter(status='available').count()
        return context


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)
