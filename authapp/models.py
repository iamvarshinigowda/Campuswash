from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)  # Additional validation recommended

    def __str__(self):
        # Use an existing field or the related user's username or first/last name
        return f"{self.user.username} ({self.phone_number})"  # Example

