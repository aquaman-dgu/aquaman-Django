from django.contrib import admin
from django.urls import path
from . import views

app_name = 'disease'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', views.main_view, name='main'),
    path('upload_csv/', views.main_view, name='upload_csv'),
    path('result/', views.result_view, name='result'),
]