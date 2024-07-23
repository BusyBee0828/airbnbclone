from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# Create your views here.
def see_all_rooms(request):
    rooms = Room.objects.all()  # 모든 방을 검색 
    return render(request, "all_rooms.html", {'rooms': rooms, 
                                              'title': "hello, this title comes from django"})
    # render 함수에 템플릿 이름을 적어둠 
    
# request object 제공: 누가 이 페이지를 요청하고, 어떤 데이터가 전송되고 있는지 등을 알 수 있다 

def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)  # room_pk에 해당하는 room을 DB에서 찾는다 
        return render(request, "room_detail.html", {'room':room,},)  # 위 DB를 템플릿으로 렌더링한다 
    except Room.DoesNotExist:
        return render(request, "room_detail.html", {'not_found': True,},)
    # DoesNotExist 에러가 발생하면: room_detail.html의 'not_found'로 렌더링