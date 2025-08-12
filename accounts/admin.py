# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Добавляем поле telegram_chat_id в админку
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("telegram_chat_id",)}),)

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("telegram_chat_id",)}),
    )

    list_display = ["email", "username", "is_staff", "telegram_chat_id"]
    search_fields = ["email", "username", "telegram_chat_id"]


admin.site.register(CustomUser, CustomUserAdmin)
