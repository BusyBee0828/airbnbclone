from rest_framework import serializers
from .models import Booking
from django.utils import timezone

class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "experience_time", "guests",)

class CreateRoomBookingSerializer(serializers.ModelSerializer):
    
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    # check_in, check_out은 필수로 넣어줘야함
    
    class Meta:
        model = Booking
        fields = ("check_in", "check_out", "guests",)  # user에게 받는 데이터들만
    
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value
    
    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value
    
    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError("Check-in should be smaller than check-out.")
        if Booking.objects.filter(check_in__lte=data["check_out"], check_out__gte=data["check_in"]).exists():
            raise serializers.ValidationError("(Some of) those dates are already taken.")
        return data