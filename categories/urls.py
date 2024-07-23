from django.urls import path
from . import views

urlpatterns = [
     path("", views.categories),
     # '/' 페이지에 오면: views.py 파일의 categories 함수를 실행하라 
     
     path("<int:pk>", views.category),
     # url에서 int를 받으면: categories_pk 변수에 넣고, views.py 파일의 category 함수를 실행하라 
]




