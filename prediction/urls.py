from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('main/', views.main_view, name='main'),
    path('result/', views.result_view, name='result'),
]