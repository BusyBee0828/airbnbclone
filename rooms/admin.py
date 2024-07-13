from django.contrib import admin
from .models import Room, Amenity 


@admin.register(Room)  # 이 클래스는 Room 모델의 admin을 컨트롤한다 
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "kind", "created_at", "updated_at", )
    list_filter = ("country", "city", "price", "kind", "pet_friendly", "amenities", "updated_at",)
    # 다른 모델들을 필터링의 조건으로 사용할 수 있다 

@admin.register(Amenity)  # 이 클래스는 Amenity 모델의 admin을 컨트롤한다 
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at",)
    readonly_fields = ("created_at", "updated_at",)