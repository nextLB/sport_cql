from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from django.views import View


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, '注册成功！请登录。')
            return redirect('users:login')
        return render(request, 'users/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.status == 'disabled':
                    messages.error(request, '该账号已被禁用，请联系管理员。')
                    return render(request, 'users/login.html', {'form': form})
                login(request, user)
                messages.success(request, f'欢迎回来，{user.username}！')
                return redirect('home')
            else:
                messages.error(request, '用户名或密码错误，请重新输入。')
        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, '您已成功退出登录。')
        return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人信息更新成功！')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.GET.get('username')
        role = self.request.GET.get('role')
        if username:
            queryset = queryset.filter(username__icontains=username)
        if role:
            queryset = queryset.filter(role=role)
        return queryset
