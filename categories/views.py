from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

@api_view(["GET", "POST"])
def categories(request):
# 데이터베이스에 있는 모든 카테고리를 가져와서 serializer에게 전달     
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)  # JSON으로 응답한다
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)   # user가 보낸 데이터를 serializer에 전달 
        if serializer.is_valid():                            # serializer는 데이터가 유효한지 확인
            return Response({'created: True'})
        else:
            return Response(serializer.errors)
       


@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)




