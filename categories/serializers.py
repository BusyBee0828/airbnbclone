from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    
# serializer 만들기
# - 카테고리(의 name, kind)가 API의 바깥 세상으로 나갈때 어떻게 표시될 지
# - 카테고리의 필드 중에 어떤 부분을 보여줄지

