from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Image


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'full_name', 'is_staff', 'is_active']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Image)
