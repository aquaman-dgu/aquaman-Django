from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

#로그인 필요
@login_required
def main_view(request):
    # 유저 메인 화면 렌더링
    return render(request, 'disease/main.html')