from django.db import models

# Create your models here.
from django.db import models
from authapp.models import Profile


class LaundryOrder(models.Model):
    orderId = models.AutoField(primary_key=True)  # Auto-generated Order ID
    userId = models.CharField(max_length=20)  # User ID as a primary key
    name = models.CharField(max_length=100)
    clothesCount = models.IntegerField()
    extras = models.CharField(max_length=20, blank=True, null=True)
    checkInDate = models.DateField()
    checkInTime = models.TimeField()

    def __str__(self):
        return f"Order {self.orderId} - User {self.userId}"
from django.db import models
from django.contrib.auth.models import User

class Membership(models.Model):
    MEMBERSHIP_CHOICES = [
        ('6_months', '6 Months'),
        ('12_months', '12 Months'),
    ]

    membership_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Fetch name, contact, etc., from User model
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    start_date = models.DateField()
    valid_until = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.membership_type}"
