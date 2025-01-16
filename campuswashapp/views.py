from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .decorators import membership_required 

def home(request):
    return render(request, 'user/home.html')  # Render the home page.




@membership_required
def laundryorders(request):
    # Logic for laundry orders
    return render(request, 'user/laundryorders.html')

 
@membership_required
def extra_services(request):
    # Logic for extra services
    return render(request, 'extra_services.html')


@membership_required
def feedback(request):
    # Logic for feedback
    return render(request, 'feedback.html')


def membership(request):
    if request.method == 'POST':
        # Collecting form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        register_number = request.POST.get('register_number')
        membership_type = request.POST.get('membership_type')

        # Determine the amount and validity date
        if membership_type == '6_months':
            amount = 2500
            validity_date = datetime.now() + timedelta(days=183)  # 6 months
        elif membership_type == '12_months':
            amount = 5000
            validity_date = datetime.now() + timedelta(days=365)  # 12 months
        else:
            amount = 0
            validity_date = None

        # Store membership details in session or pass it to the payment view
        request.session['membership_details'] = {
            'name': name,
            'email': email,
            'contact_number': contact_number,
            'register_number': register_number,
            'membership_type': membership_type,
            'amount': amount,
            'validity_date': validity_date.strftime('%Y-%m-%d')  # Convert date to string
        }

        return render(request, 'user/payment.html', {
            'amount': amount,
            'validity_date': validity_date.strftime('%Y-%m-%d')
        })

    return render(request, 'user/membership.html')

def payment(request):
    if request.method == 'POST':
        # Process the payment here
        # Redirect to the home page after payment
        return redirect('home')

    return render(request, 'user/payment.html')
