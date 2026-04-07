from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Venue, VenueSpace
from .forms import VenueForm, VenueSpaceForm, VenueSpaceFilterForm
from .forms import VenueForm, VenueSpaceForm, VenueSpaceFilterForm


class VenueListView(ListView):
    model = Venue
    template_name = 'venues/venue_list.html'
    context_object_name = 'venues'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Venue.objects.filter(status='open')
        venue_type = self.request.GET.get('type')
        keyword = self.request.GET.get('keyword')
        
        if venue_type:
            queryset = queryset.filter(venue_type=venue_type)
        if keyword:
            queryset = queryset.filter(models.Q(name__icontains=keyword) | models.Q(address__icontains=keyword))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['venue_types'] = Venue.TYPE_CHOICES
        context['current_type'] = self.request.GET.get('type', '')
        context['keyword'] = self.request.GET.get('keyword', '')
        return context


class VenueDetailView(DetailView):
    model = Venue
    template_name = 'venues/venue_detail.html'
    context_object_name = 'venue'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venue_spaces = self.object.venue_spaces.all()
        status_filter = self.request.GET.get('status')
        if status_filter:
            venue_spaces = venue_spaces.filter(status=status_filter)
        context['venue_spaces'] = venue_spaces
        context['space_status_choices'] = VenueSpace.STATUS_CHOICES
        return context


@login_required
def venue_create(request):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('home')
    
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            if Venue.objects.filter(name=form.cleaned_data['name']).exists():
                messages.error(request, '场馆名称已存在，请重新输入。')
            else:
                form.save()
                messages.success(request, '场馆添加成功！')
                return redirect('venues:venue_list')
    else:
        form = VenueForm()
    return render(request, 'venues/venue_form.html', {'form': form, 'action': '添加'})


@login_required
def venue_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('home')
    
    venue = get_object_or_404(Venue, pk=pk)
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            old_name = venue.name
            new_name = form.cleaned_data['name']
            if old_name != new_name and Venue.objects.filter(name=new_name).exists():
                messages.error(request, '场馆名称已存在，请重新输入。')
            else:
                form.save()
                messages.success(request, '场馆信息更新成功！')
                return redirect('venues:venue_list')
    else:
        form = VenueForm(instance=venue)
    return render(request, 'venues/venue_form.html', {'form': form, 'action': '编辑'})


@login_required
def venue_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('home')
    
    venue = get_object_or_404(Venue, pk=pk)
    if request.method == 'POST':
        if venue.venue_spaces.exists():
            messages.error(request, '请先删除该场馆下的所有场地后再操作。')
            return redirect('venue_edit', pk=pk)
        venue.delete()
        messages.success(request, '场馆删除成功！')
        return redirect('venues:venue_list')
    return render(request, 'venues/venue_confirm_delete.html', {'venue': venue})


class VenueSpaceListView(ListView):
    model = VenueSpace
    template_name = 'venues/space_list.html'
    context_object_name = 'spaces'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = VenueSpace.objects.all()
        venue_id = self.request.GET.get('venue')
        status = self.request.GET.get('status')
        
        if venue_id:
            queryset = queryset.filter(venue_id=venue_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['venues'] = Venue.objects.all()
        context['filter_form'] = VenueSpaceFilterForm(self.request.GET)
        return context


@login_required
def venue_space_create(request):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('home')
    
    if request.method == 'POST':
        form = VenueSpaceForm(request.POST)
        if form.is_valid():
            venue = form.cleaned_data['venue']
            name = form.cleaned_data['name']
            if VenueSpace.objects.filter(venue=venue, name=name).exists():
                messages.error(request, f'该场馆下已存在同名场地"{name}"，请重新输入。')
            else:
                form.save()
                messages.success(request, '场地添加成功！')
                return redirect('venues:space_list')
    else:
        form = VenueSpaceForm()
    return render(request, 'venues/space_form.html', {'form': form, 'action': '添加'})


@login_required
def venue_space_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('home')
    
    space = get_object_or_404(VenueSpace, pk=pk)
    if request.method == 'POST':
        form = VenueSpaceForm(request.POST, instance=space)
        if form.is_valid():
            old_venue = space.venue
            old_name = space.name
            new_venue = form.cleaned_data['venue']
            new_name = form.cleaned_data['name']
            if (old_venue != new_venue or old_name != new_name) and \
               VenueSpace.objects.filter(venue=new_venue, name=new_name).exclude(pk=pk).exists():
                messages.error(request, f'该场馆下已存在同名场地"{new_name}"，请重新输入。')
            else:
                form.save()
                messages.success(request, '场地信息更新成功！')
                return redirect('venues:space_list')
    else:
        form = VenueSpaceForm(instance=space)
    return render(request, 'venues/space_form.html', {'form': form, 'action': '编辑'})


@login_required
def venue_space_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面。')
        return redirect('home')
    
    space = get_object_or_404(VenueSpace, pk=pk)
    if request.method == 'POST':
        space.delete()
        messages.success(request, '场地删除成功！')
        return redirect('venues:space_list')
    return render(request, 'venues/space_confirm_delete.html', {'space': space})


@require_http_methods(["GET"])
def get_available_times(request):
    space_id = request.GET.get('space_id')
    date = request.GET.get('date')
    
    if not space_id or not date:
        return JsonResponse({'error': '参数不完整'}, status=400)
    
    from bookings.models import Booking
    from datetime import datetime, timedelta
    
    try:
        space = VenueSpace.objects.get(pk=space_id)
        booking_date = datetime.strptime(date, '%Y-%m-%d').date()
        
        if booking_date < datetime.now().date():
            return JsonResponse({'error': '不能预约过去的时间'}, status=400)
        
        all_times = []
        start_hour = 9
        end_hour = 22
        
        for hour in range(start_hour, end_hour):
            time_slot = f"{hour:02d}:00-{hour+1:02d}:00"
            
            is_booked = Booking.objects.filter(
                space=space,
                booking_date=booking_date,
                time_slot__startswith=f"{hour:02d}:",
                status__in=['pending', 'confirmed']
            ).exists()
            
            all_times.append({
                'time': time_slot,
                'hour': hour,
                'available': not is_booked and space.status == 'available'
            })
        
        return JsonResponse({'times': all_times, 'space_status': space.status})
    except VenueSpace.DoesNotExist:
        return JsonResponse({'error': '场地不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
