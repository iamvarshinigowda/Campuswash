from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db import models

class UserRegistration(models.Model):
    # Register Number as Primary Key
    register_number = models.CharField(max_length=50, primary_key=True)
    
    # Name of the user
    name = models.CharField(max_length=100)
    
    # Email ID with unique constraint
    email = models.EmailField(unique=True)
    
    # Contact number
    contact_number = models.CharField(max_length=15)
    
    # Password (hashed)
    password = models.CharField(max_length=128)
    
    # Role (admin or user)
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Add missing fields for authentication
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        """Hash the raw password and store it in the password field."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.register_number}) - {self.role}"


from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_expiry = models.DateField(null=True, blank=True)

    @property
    def has_membership(self):
        return self.membership_expiry and self.membership_expiry >= date.today()
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
