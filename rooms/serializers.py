from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from rest_framework import serializers
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description")
        

class RoomListSerializer(serializers.ModelSerializer):
    
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
           
    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city", "price", "rating", "is_owner", "photos")
    
    def get_rating(self, room):
        return room.rating()
    
    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user

class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True,)
    amenities = AmenitySerializer(read_only=True, many=True)    
    category = CategorySerializer(read_only=True,)
    
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()  # 위시리스트에서 '좋아요' 
    photos = PhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Room
        fields = "__all__"
        
    def get_rating(self, room):
        return room.rating()
    
    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user
    
    def get_is_liked(self, room):
        request = self.context['request']
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk,).exists()
        # 예를 들어, room name이 'Apartment in Seoul'인 room이 들어있는 위시리스트를 필터링할 수 있다