from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomListSerializer
from .models import Wishlist

class WishlistSerializer(ModelSerializer):
    
    rooms = RoomListSerializer(many=True, read_only=True)
    # read_only=True: 위시리스트 만들때는 rooms에 대해서 read_only 이어야 
    
    class Meta:
        model = Wishlist 
        fields = ("pk", "name", "rooms")