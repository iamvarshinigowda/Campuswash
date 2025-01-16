from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserRegistration
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .models import UserRegistration

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('userType').strip().lower()  # Normalize case

        try:
            # Find user by email
            user = UserRegistration.objects.get(email=email)
            if user.check_password(password):  # Check password validity
                # Authenticate the user (set the backend to your custom backend)
                user.backend = 'authapp.backends.CustomBackend'  # Specify your custom backend
                if user.role == 'admin' and user_type == 'admin':
                    auth_login(request, user)  # Login user with the custom backend
                    return redirect('admin_home')  # Redirect to admin home
                elif user.role == 'user' and user_type == 'user':
                    auth_login(request, user)  # Login user with the custom backend
                    return redirect('home')  # Redirect to user home
                else:
                    return HttpResponse("Invalid role or user type.", status=400)
            else:
                return HttpResponse("Invalid password.", status=400)
        except UserRegistration.DoesNotExist:
            return HttpResponse("User does not exist.", status=400)

    # Render the login page for GET requests
    return render(request, 'authenticate/login.html')

# Register View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserRegistration
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserRegistration
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        register_number = request.POST.get('register_number')  # Corrected field name
        email = request.POST.get('email')
        contact_number = request.POST.get('contact')
        password = request.POST.get('password')

        # Validate presence of fields
        if not name or not register_number or not email or not contact_number or not password:
            return HttpResponse("All fields are required.")  # Optionally redirect to the form with an error message

        # Strip whitespace from input values
        name = name.strip()
        register_number = register_number.strip()
        email = email.strip()
        contact_number = contact_number.strip()
        password = password.strip()

        # Check if the register number or email already exists
        if UserRegistration.objects.filter(register_number=register_number).exists():
            return HttpResponse("Register number already exists.")
        if UserRegistration.objects.filter(email=email).exists():
            return HttpResponse("Email already exists.")

        # Create a new user
        user = UserRegistration(
            register_number=register_number,
            name=name,
            email=email,
            contact_number=contact_number,
        )
        user.set_password(password)  # Ensure password is hashed
        user.save()

        # Optionally set the last_login field to the current timestamp (if needed)
        user.last_login = timezone.now()
        user.save()

        # Redirect to login page after successful registration
        return redirect('login')

    # Render registration page for GET requests
    return render(request, 'authenticate/register.html')
  # Ensure this template exists

# Home View
def home(request):
    return render(request, 'user/home.html')  # Update with the correct home template
