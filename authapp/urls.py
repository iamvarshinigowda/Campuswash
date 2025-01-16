from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login, register, home

urlpatterns = [
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('', home, name='home'),  # Ensure this URL points to the correct template
    
]
