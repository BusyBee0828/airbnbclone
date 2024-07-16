from django.db import models
from common.models import CommonModel

class Booking(CommonModel):
    """Booking Model Definition"""
    
    class BookingKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")
    
    kind = models.CharField(max_length=15, choices=BookingKindChoices.choices,)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='bookings')
    # 만약 user가 삭제되면 booking 정보도 삭제된다 
    room = models.ForeignKey("rooms.Room", null=True, blank=True, on_delete=models.SET_NULL, related_name='bookings')
    # experience만 예약하는 경우 room은 null이 될 수 있다 
    # room이 삭제되어도 booking 정보는 남아있다 
    experience = models.ForeignKey("experiences.Experience", null=True, blank=True, on_delete=models.SET_NULL, related_name='bookings')
    # experience도 room과 같다
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    experience_time = models.DateTimeField(null=True, blank=True)
    guests = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.kind.title()} booking for: {self.user}"
    
    
    
    