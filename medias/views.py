from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .models import Photo

class PhotoDetail(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound
    
    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.room:                              # photo가 room을 가지고 있고 
            if photo.room.owner != request.user:    # 그 room의 owner가 request의 user와 다르다면
                raise PermissionDenied
        elif photo.experience:
            if photo.experience.host != request.user:
                raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)