from django.contrib import admin
from .models import Experience, Perk

@admin.register(Experience)    # 이 클래스는 Experience 어드민 패널을 컨트롤한다 
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "start", "end", "created_at")
    list_filter = ("category",)


@admin.register(Perk)    # 이 클래스는 Perk 어드민 패널을 컨트롤한다 
class PerkAdmin(admin.ModelAdmin):
    list_display = ("name", "details", "explanation")
    
