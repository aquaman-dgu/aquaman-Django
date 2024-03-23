from django.urls import path
from recognition import views

urlpatterns = [
    path('', views.recognition_view, name='recognition_view'),  # 'recognition' 앱의 메인 페이지에 대한 URL
]