from django.db import transaction
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from .models import Amenity, Room
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from categories.models import Category
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer

class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data,)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)
    
    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True,)
        # (데이터베이스의 amenity, user가 보낸 데이터, 부분업데이트라는 것을 알림)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data,)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
    
class Rooms(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    # GET request는 누구나 ㅇㅋ
    # POST, PUT, DELETE request는 인증받은 사람들 only 
    
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True, context={'request':request})
        return Response(serializer.data)
    
    def post(self, request):
        
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            try:
                with transaction.atomic():  # transaction.atomic 안의 코드는 데이터베이스에 바로 반영되지 X 
                    room = serializer.save(owner=request.user, category=category)  
                    # owner=request.user: 자동으로 owner를 room에 추가 
                
                    amenities = request.data.get("amenities") 
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)

                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found")
            
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RoomDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
            
    
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:  # request한 user가 room owner가 아니면 에러메세지 
            raise PermissionDenied
        
        serializer = RoomDetailSerializer(room, data=request.data, partial=True,)

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError(detail="Category not found")

            try:
                with transaction.atomic():
                    if category_pk:
                        room = serializer.save(category=category)
                    else:
                        room = serializer.save()

                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)

                    return Response(RoomDetailSerializer(room).data)
            except Exception as e:
                print(e)
                raise ParseError("amenity not found")
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            
    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:  # request한 user가 room owner가 아니면 에러메세지 
            raise PermissionDenied
        room.delete()                   # 위 두 조건을 확인한 후 delete 실행 
        return Response(status=HTTP_204_NO_CONTENT)
    
    
class RoomReviews(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        try:
            page = request.query_params.get("page",1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page-1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(room.reviews.all()[start:end], many=True,)
        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=self.get_object(pk))
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        

class RoomPhotos(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    
    def post(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:  # 유저 인증 확인 
            raise NotAuthenticated
        if request.user != room.owner:         # room owner 여부 확인 
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)  # 파일과 설명만 가진 사진을 만든다 
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        

class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound
    
    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(room=room, kind=Booking.BookingKindChoices.ROOM, check_in__gt=now,)
        # check_in__gt=now: 체크인이 now보다 큰 경우만 필터링
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = PublicBookingSerializer(data=request.data)
        if serializer.is_valid():
            pass
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(room=room, user=request.user,kind=Booking.BookingKindChoices.ROOM,)
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        # is_valid(): 미래의 날짜만 체크인할 수 있다는 것을 할 줄 모르기 때문에 validation을 customize해서 추가해야
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        # bookings의 모델에서는 only "guests" is required 