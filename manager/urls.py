from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'manager'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('main/', views.main_view, name='main'),
    path('logout/', LogoutView.as_view(next_page='manager:login'), name='logout'),
]