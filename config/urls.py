"""
URL configuration for config project.

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
    path('api/v1/rooms/', include("rooms.urls")),
    # 누가 'rooms/~~'로 접속하면: rooms의 urls.py의 파일을 살펴봐라
    
    path('api/v1/categories/', include('categories.urls')),
    # api를 제공하는 url 임을 명시 
    
    # 작업할 때마다 새로운 버전을 만들어서 저장
]




