from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', include('users.urls', namespace='users')),
    path('venues/', include('venues.urls', namespace='venues')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
