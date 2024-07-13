from django.db import models
from common.models import CommonModel

class Room(CommonModel):
    """Room Model Definition"""
    
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")
    
    name = models.CharField(max_length=180, default="",)             
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=20, choices=RoomKindChoices.choices)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    amenities = models.ManyToManyField("rooms.Amenity")
    # rooms.Amenity와 ManyToMany 관계를 가지는 amenities 변수를 만든다 
    category = models.ForeignKey("categories.Category", null=True, blank=True, on_delete=models.SET_NULL)
    # on_delete=models.SET_NULL: category가 없어져도 Experience는 그대로 있다 
    
    def __str__(self) -> str:
        return self.name
    # Room을 등록했을 때, 'name'이 str로 나타나게한다 
    

class Amenity(CommonModel):
    """Amenity Definition"""
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name 
    # Amenity를 등록했을 때, 'name'이 str로 나타나게한다 
    
    class Meta:
        verbose_name_plural = "Amenities"
    # 어드민 패널에서 'Amenitys' -> 'Amenities'로 수정