from django.db import models
from common.models import CommonModel

class Experience(CommonModel):
    """Experience Model Definition"""
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    name = models.CharField(max_length=250,)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    # on_delete=models.CASCADE: host가 없어지면 Experience도 없어진다 
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField() 
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk", null=True, blank=True)
    # Perk 클래스에서 여러개 가져올 수 있다 
    category = models.ForeignKey("categories.Category", null=True, blank=True, on_delete=models.SET_NULL)
    # on_delete=models.SET_NULL: category가 없어져도 Experience는 그대로 있다 
    
    def __str__(self) -> str:
        return self.name
    
    
    
class Perk(CommonModel):
    """What is included on an Experience"""
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    def __str__(self) -> str:
        return self.name
    
    
    
    