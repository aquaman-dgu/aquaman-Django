from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('user:main')
    
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:main')
        else:
            error_message = "Invalid username or password"
    return render(request, 'user/login.html', {'error_message' : error_message})

def logout_view(request):
    logout(request)
    return redirect('user:login')  # 로그인 페이지 또는 홈 페이지로 리디렉트

def signup_view(request):
    # 유저 회원가입 처리
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # 회원가입 후 로그인 페이지로 리디렉션
            return redirect('user:signup_success')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})


def signup_success(request):
    return render(request, 'user/signup_success.html')

#로그인 필요
@login_required
def main_view(request):
    # 유저 메인 화면 렌더링
    return redirect('recognition:main')