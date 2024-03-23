from django.urls import path
from main import views

urlpatterns = [
    path('', views.main_view, name='main_view'),  # 'main' 앱의 메인 페이지에 대한 URL
]
