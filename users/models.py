from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):  # AbstractUser에서 상속받아 User 클래스를 만든다 
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")  # ("데이터베이스에 들어갈 value", "패널에 노출될 label")
        FEMALE = ("female", "Female")
    
    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")
    
    class CurrencyChoices(models.TextChoices):
        WON = ("won", "Korean Won")
        USD = ("usd", "US Dollar")
    
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    avatar = models.URLField(blank=True)   # blank=True: 이미지 첨부가 필수가 X 
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    currency = models.CharField(max_length=5, choices=CurrencyChoices.choices)