from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    file = models.ImageField()
    description = models.CharField(max_length=140,)
    room = models.ForeignKey("rooms.Room", null=True, blank=True, on_delete=models.CASCADE)
    experience = models.ForeignKey("experiences.Experience", null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Photo File"
    

class Video(CommonModel):   # video는 experience에만 
    file = models.FileField()
    experience = models.OneToOneField("experiences.Experience", on_delete=models.CASCADE)
    # OneToOneField: 하나의 동영상은 하나의 experience에 연결(하나의 experience는 하나의 video만 가질 수 있다)
    # OneToOneField: ForeignKey와 같은 기능을 하나 1-1의 고유 연결을 할 때(결제정보 등)
    
    def __str__(self):
        return "Video File"
    
    
    