from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('main/', views.main_view, name='main'),
]