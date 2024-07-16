from django.db import models
from common.models import CommonModel
from django.db.models import Avg


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
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="rooms")
    amenities = models.ManyToManyField("rooms.Amenity", related_name='rooms')
    # rooms.Amenity와 ManyToMany 관계를 가지는 amenities 변수를 만든다 
    category = models.ForeignKey("categories.Category", null=True, blank=True, on_delete=models.SET_NULL, related_name='rooms')
    # on_delete=models.SET_NULL: category가 없어져도 Experience는 그대로 있다 
    
    def __str__(self) -> str:
        return self.name
    # Room을 등록했을 때, 'name'이 str로 나타나게한다 
    
    def total_amenities(self):
        return self.amenities.count()
    
    # def rating(self):
    #     count = self.reviews.count()
    #     # review 모델에서 related_name='reviews'라고 바꿔줘서 위와 같이 하면 된다 
    #     # related_name을 설정하지 않았다면 default로 'review_set'으로 되어있다 
    #     if count == 0:
    #         return "No Reviews"
    #     else:
    #         total_rating = 0
    #         for review in self.reviews.all().values("rating"):
    #             total_rating += review['rating']
    #         return round(total_rating / count, 1)
    #     # .values("rating")가 없으면: reviews에 있는 모든 데이터를 가져오게되어 비효율적 
    #     # 이제 리뷰의 rating만을 가져온다
    #     # 단, 이제 review가 딕셔너리가 되어서 review['rating']으로 가져온다
    
    
    def rating(self):
        average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if average_rating is None:
            return "No Reviews"
        else:
            return round(average_rating, 1)
        

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