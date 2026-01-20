from django.conf import settings
from django.db import models
from django.utils import timezone

class Log(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=120)
    date_action = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date_action:%Y-%m-%d %H:%M} - {self.action}"
