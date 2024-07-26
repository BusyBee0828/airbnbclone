from django.urls import path
from . import views

urlpatterns = [
     path("", views.CategoryViewSet.as_view({'get': 'list',          # get 요청을 받으면: list 메서드를 실행 
                                             'post': 'create',})),   # post 요청을 받으면: create 메서드를 실행 
     # '/' 페이지에 오면: CategoryViewSet 클래스를 실행  
     
     path("<int:pk>", views.CategoryViewSet.as_view({'get': 'retrieve',
                                                     'put': 'partial_update',
                                                     'delete': 'destroy',})),
     # url에서 int를 받으면: categories_pk 변수에 넣고, views.py 파일의 CategoryViewSet 클래스를 실행
]




