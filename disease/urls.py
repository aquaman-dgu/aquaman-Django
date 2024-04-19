from django.urls import path
from . import views

app_name = 'disease'

urlpatterns = [
    path('main/', views.main_view, name='main'),
]