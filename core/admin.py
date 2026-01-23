from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("date_action", "user", "action")
    search_fields = ("action", "details", "user__username")
    list_filter = ("action",)
