from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import UserProfile  # Import the UserProfile model correctly

# View for user registration
def register(request):
    if request.method == 'POST':
        register_number= request.POST['register_number']
        name= request.POST['name']
        email= request.POST['email']
        phone= request.POST['phone_number']
        password= request.POST['password']
        user = User.objects.create(username=email, email=email, first_name=name, last_name=register_number)
        user.set_password(password)
        user.save()

        userProfile = UserProfile.objects.create(user=user, phone_number=phone)
        userProfile.save()
            # Create a UserProfile instance for the registered user
            # UserProfile.objects.create(user=user)
        return redirect('login')  # Replace 'home' with your actual homepage URL name
    else:
        return render(request, 'authenticate/register.html')

def user_login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin')
                else:
                    return redirect('home')  
            else:
                return redirect('login')
        else:
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html')

# @login_required(login_url='login')from django.shortcuts import render

def home(request):
    return render(request, 'user/home.html')  # Replace 'home.html' with the correct template
