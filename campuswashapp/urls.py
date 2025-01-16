from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, laundryorders, feedback, payment, membership

urlpatterns = [
    path('', home, name='home'),  # Main app home
    path('laundryorders', laundryorders, name='laundryorders'),
    path('feedback', feedback, name='feedback'),
    path('payment', payment, name='payment'),
    path('membership', membership, name='membership'),
    path('login/', LoginView.as_view(template_name='authenticate/login.html'), name='login'),  # Login page
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout page
]
