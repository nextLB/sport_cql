from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import User
from .forms import UserRegistrationForm


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
        return redirect('profile')
    return render(request, 'users/profile_edit.html')


@login_required
def change_password(request):
    from django.contrib.auth.views import PasswordChangeView
    from django.urls import reverse_lazy
    
    class PasswordChange(PasswordChangeView):
        template_name = 'users/password_change.html'
        success_url = reverse_lazy('profile')
    
    return PasswordChange.as_view()(request)
