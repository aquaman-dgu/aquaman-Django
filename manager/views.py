from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_view(request):
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

@login_required
def main_view(request):
    # 유저 관리 화면 렌더링
    return render(request, 'manager/main.html')