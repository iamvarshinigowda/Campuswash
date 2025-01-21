from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import home, laundryorders, payment, create_membership, user_logout, extra_service_view,feedback_view,admin_dash
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', home, name='home'),  # Main app home
    path('laundryorders', laundryorders, name='laundryorders'),
    path('feedback',feedback_view , name='feedback'),
    path('payment', payment, name='payment'),
    path('membership', create_membership, name='membership'),
    path('extraservice',extra_service_view, name='extraservice'),
    path('login/', LoginView.as_view(template_name='authenticate/login.html'), name='login'),  # Login page
    path('logout/', user_logout, name='logout'),  # Logout page
    path('admin-dash',admin_dash, name='admin_dash'),  # User profile page
    
  
]

