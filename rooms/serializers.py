from rest_framework.serializers import ModelSerializer
from .models import Amenity

class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"  # 모든 필드를 노출한다 