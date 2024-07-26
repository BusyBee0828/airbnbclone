from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
    # serializer가 category model을 위한 serializer를 만들어준다 
    # (models.py에 있는 것들을 자동으로 가져온다)
    
        fields = "__all__"
        # fields = "__all__": 모두 표시 
        # fields = ("name", "kind"): 무엇을 나타낼 지 지정 
        
        
        
        