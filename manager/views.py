from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('manager:main')
    
    error_message = None
    
    # 로그인 처리
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # staff 사용자만 로그인 허용
            login(request, user)
            return redirect('manager:main')
        else:
            error_message = "Invalid username or password"
    return render(request, 'manager/login.html', {'error_message' : error_message})

def logout_view(request):
    logout(request)
    return redirect('manager:login')  # 로그인 페이지 또는 홈 페이지로 리디렉트

@login_required
def main_view(request):    
    query = request.GET.get('q', '')  # 검색창에서 입력받은 값을 가져옵니다.
    if query:
        users = User.objects.filter(is_staff=False, username__icontains=query)  # 대소문자 구분 없이 검색
    else:
        users = User.objects.filter(is_staff=False)  # 검색창이 비어있을 때 모든 사용자를 표시
    
    return render(request, 'manager/main.html', {'users': users})