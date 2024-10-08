from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("Profile", {"fields": ("username", "password", "name", "avatar", "email", "is_host", "gender", "language", "currency",),},),
        ("permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions",),
                         "classes": ("collapse",),},),
        ("Important dates", {"fields": ("last_login", "date_joined"),
                             "classes": ("collapse",),},),
        )

    list_display = ("username", "email", "name", "is_host")
    
    
# admin.site.register(User, UserAdmin)
