from django.db import models

class CommonModel(models.Model):
    """Common Model Definition"""
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True: object가 처음으로 생성된 시각을 추가 
    updated_at = models.DateTimeField(auto_now=True)
    # auto_now=True: object가 업데이트된 시각을 추가 
    
    class Meta:
        abstract = True   # 이 모델은 데이터베이스에 저장되지 않는다 