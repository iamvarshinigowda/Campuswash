from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import UserRegistration
from django.contrib.auth import get_user_model

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = UserRegistration.objects.get(email=email)  # Search by email
            if user.check_password(password):  # Check if the password matches
                return user
            return None
        except UserRegistration.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserRegistration.objects.get(id=user_id)  # Return user by id
        except UserRegistration.DoesNotExist:
            return None
