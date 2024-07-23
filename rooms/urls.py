from django.urls import path
from . import views

urlpatterns = [
    path("", views.see_all_rooms),
    path("<int:room_pk>", views.see_one_room),
    # <parameter type:parameter name>
    # rooms/1 이런식으로 'rooms/ + int'가 오면: views 파일의 see_one_room 함수를 실행 
    # 'rooms/str'로도 path를 만들 수 있다(원하는 타입으로 가능)
    # "<int:room_id>/<str:room_name>" 으로도 가능 
]



