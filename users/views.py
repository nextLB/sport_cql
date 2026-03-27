from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import User
from .forms import UserRegistrationForm
from bookings.models import Booking


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        if self.request.user.user_type == 'admin':
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, '用户名或密码错误')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '注册成功！请登录')
        return response


@login_required
def profile(request):
    return render(request, 'users/profile.html', {
        'user': request.user
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.save()
        messages.success(request, '个人信息更新成功')
        return redirect('users:profile')
    return render(request, 'users/profile_edit.html')


@login_required
def change_password(request):
    from django.contrib.auth.views import PasswordChangeView
    from django.urls import reverse_lazy
    
    class PasswordChange(PasswordChangeView):
        template_name = 'users/password_change.html'
        success_url = reverse_lazy('profile')
    
    return PasswordChange.as_view()(request)


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def user_list(request):
    users = User.objects.all().order_by('-created_at')
    user_type = request.GET.get('user_type')
    search = request.GET.get('search')
    
    if user_type:
        users = users.filter(user_type=user_type)
    if search:
        users = users.filter(username__icontains=search)
    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'users/user_list.html', {
        'page_obj': page_obj,
        'user_type': user_type,
        'search': search
    })


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.user_type = request.POST.get('user_type', 'user')
        user.is_active = request.POST.get('is_active') == 'on'
        
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        user.save()
        messages.success(request, f'用户 {user.username} 信息已更新')
        return redirect('users:user_list')
    
    booking_count = Booking.objects.filter(user=user).count()
    return render(request, 'users/user_edit.html', {
        'edit_user': user,
        'booking_count': booking_count
    })


@user_passes_test(lambda u: u.is_staff or u.user_type == 'admin')
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if user == request.user:
        messages.error(request, '不能删除自己的账号')
        return redirect('user_list')
    
    username = user.username
    user.delete()
    messages.success(request, f'用户 {username} 已删除')
    return redirect('users:user_list')
