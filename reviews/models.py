from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator  # validators 추가
from common.models import CommonModel


class Review(CommonModel):
    """Review from a User to a Room or Experience"""
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='reviews')
    room = models.ForeignKey("rooms.Room", null=True, blank=True, on_delete=models.CASCADE, related_name='reviews')
    experience = models.ForeignKey("experiences.Experience", null=True, blank=True, on_delete=models.CASCADE, related_name='reviews')
    payload = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    
    def __str__(self) -> str:
        return f"{self.user} / {self.rating}"