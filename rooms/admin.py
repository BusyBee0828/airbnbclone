from django.contrib import admin
from .models import Room, Amenity 

@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    # model_admin: 이 액션을 호출하는 클래스 
    # request: 이 액션을 누가 호출했는지
    # rooms: 내가 선택한 모든 객체 리스트 
    for room in rooms.all():
        room.price = 0
        room.save()
    # admin panel에서 선택하여 실행한 room의 가격이 0이 된다 


@admin.register(Room)  # 이 클래스는 Room 모델의 admin을 컨트롤한다 
class RoomAdmin(admin.ModelAdmin):
    
    actions = (reset_prices,)
    
    list_display = ("name", "price", "kind", "total_amenities", "rating", "owner", "created_at",)
    list_filter = ("country", "city", "price", "kind", "pet_friendly", "amenities", "updated_at",)
    # 다른 모델들을 필터링의 조건으로 사용할 수 있다 
    
    search_fields = ("name", "price", "owner__username")
    # "name": "name" 필드의 단어를 포함하는 결과를 출력(contains)
    # "^name": "name" 필드의 단어로 시작하는 결과를 출력(startswith)
    # "=name": "name" 필드의 단어와 일치하는 결과를 출력(exact)
    # "owner__username": owner의 username으로 검색(contains)
    
    
    def total_amenities(self, room):
        return room.amenities.count()

@admin.register(Amenity)  # 이 클래스는 Amenity 모델의 admin을 컨트롤한다 
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at",)
    readonly_fields = ("created_at", "updated_at",)
    
    