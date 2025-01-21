from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.exceptions import ValidationError

class laundry_Payments(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('ONLINE', 'Online'),
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
    ]

    PAYMENT_FOR_CHOICES = [
        ('ORDERS', 'Laundry Orders'),
        ('SERVICES', 'Extra Services'),
    ]

    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    payment_for = models.CharField(max_length=15, choices=PAYMENT_FOR_CHOICES)

    def __str__(self):
        return f"Payment ID: {self.payment_id}, Type: {self.payment_type}, For: {self.payment_for}"


class laundry_Membership(models.Model):
    MEMBERSHIP_CHOICES = [
        ('6M', '6 Months'),
        ('12M', '12 Months'),
    ]

    membership_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(laundry_Payments, on_delete=models.CASCADE,unique=True)
    membership_type = models.CharField(max_length=3, choices=MEMBERSHIP_CHOICES)
    start_date = models.DateField()
    valid_until = models.DateField()

    def __str__(self):
        return f"Membership ID: {self.membership_id}, Type: {self.get_membership_type_display()}"
    def clean(self):
        # Ensure a user can only have one active membership
        existing_membership = laundry_Membership.objects.filter(user=self.user).exclude(membership_id=self.membership_id)
        if existing_membership.exists():
            raise ValidationError(f"{self.user.username} already has an active membership.")

    def save(self, *args, **kwargs):
        # Automatically calculate the valid_until date based on membership_type
        from datetime import timedelta

        if self.membership_type == '6M':
            self.valid_until = self.start_date + timedelta(days=6 * 30)
        elif self.membership_type == '12M':
            self.valid_until = self.start_date + timedelta(days=12 * 30)
        super().save(*args, **kwargs)



class LaundryOrders(models.Model):
    STATUS_CHOICES = [
        ('Not Done', 'Not Done'),
        ('Done', 'Done'),
    ]

    laundry_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(laundry_Membership, on_delete=models.CASCADE)  # Assuming Membership model is defined
    clothes_count = models.PositiveIntegerField()
    extra_item = models.TextField(blank=True, null=True)  # For additional items like blankets, etc.
    check_in_date = models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(auto_now_add=True)
    check_out_date = models.DateField(null=True, blank=True)  # Default null, updated by admin
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Not Done',  # Default value for new orders
    )

    def __str__(self):
        return (
            f"Laundry ID: {self.laundry_id}, "
            
            f"Membership ID: {self.membership.membership_id}, "
            f"Status: {self.status}"
        )

    



from django.db import models
from django.contrib.auth.models import User

class ExtraService(models.Model):
    EXTRA_SERVICE_CHOICES = [
        ('dry_cleaning', 'Dry Cleaning'),
        ('ironing', 'Ironing'),
        ('folding', 'Folding'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('online', 'Online'),
        ('card', 'Card'),
        ('cash', 'Cash'),
    ]

    # Primary key will be auto-created by Django as 'id'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='extra_services')
    extraService = models.CharField(max_length=20, choices=EXTRA_SERVICE_CHOICES)
    clothesCount = models.PositiveIntegerField()
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentType = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Fix field name in the __str__ method
        return f"{self.user.username} - {self.extraService} ({self.date_requested})"

    def calculate_amount(self):
        """
        Calculates the total amount based on the service type and clothes count.
        """
        rates = {
            'dry_cleaning': 100,
            'ironing': 12,
            'folding': 3,
        }
        return rates[self.extraService] * self.clothesCount

    
    from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    FEEDBACK_CHOICES = [
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('inquiry', 'Inquiry'),
        ('appreciation', 'Appreciation'),
    ]

    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_CHOICES)
    message = models.TextField()
    rating = models.PositiveIntegerField()  # Store ratings as integers (1-5)

    def __str__(self):
        return f"{self.user.username} - {self.feedback_type}"
