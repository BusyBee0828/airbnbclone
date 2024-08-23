from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    
    user = TinyUserSerializer(read_only=True)
    # read_only=True: 유저가 payload, rating만 전송해도 serializer는 valid
    
    class Meta:
        model = Review
        fields = ("user", "payload", "rating")