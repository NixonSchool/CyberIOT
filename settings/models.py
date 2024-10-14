# settings/models.py

from django.db import models
from django.conf import settings

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_settings')
    email_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    sound_effects = models.BooleanField(default=True)
    auto_update = models.BooleanField(default=False)
    data_usage = models.BooleanField(default=True)
    location_services = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Settings"
