"""
URL configuration for aquaman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # 메인 홈페이지로 이동
    path('manager/', include('manager.urls')),  # Manager 앱으로 이동    
    path('user/', include('user.urls')),  # User 앱으로 이동,
    path('disease/', include('disease.urls')),
    path('prediction/', include('prediction.urls')),
]
