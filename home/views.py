from django.shortcuts import render

# Create your views here.
def home_view(request):
    # home 앱의 메인 페이지를 렌더링합니다.
    return render(request, 'home/index.html')