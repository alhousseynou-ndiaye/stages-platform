from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Profil", {"fields": ("role", "nom", "prenom", "telephone", "actif")}),
    )
    list_display = ("username", "email", "role", "actif", "is_staff", "is_superuser")
    list_filter = ("role", "actif", "is_staff")
