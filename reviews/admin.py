from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Review

class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"
    parameter_name = "word"
    
    def lookups(self, request, model_admin):
        return [("good", "Good"), ("great", "Great"), ("awesome", "Awesome"), ]
    # 필터에서 선택할 수 있는 옵션 정의 
    # ("내부 데이터용", "출력용")
    
    def queryset(self, request, reviews):  # 필터링된 쿼리셋을 반환
        word = self.value()  # 현재 선택된 필터 옵션의 값 
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews
    
    


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "payload")
    list_filter = ("rating", "user__is_host", "room__category", "room__pet_friendly", WordFilter,)