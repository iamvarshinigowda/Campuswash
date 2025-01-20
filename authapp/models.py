from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)  # Additional validation recommended

    def __str__(self):
        return f"{self.name} ({self.register_number})"
