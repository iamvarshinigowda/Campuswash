from django.shortcuts import render, redirect
from datetime import datetime, timedelta,date
from .decorators import membership_required 
from .models import laundry_Payments,laundry_Membership 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import laundry_Membership, LaundryOrders ,ExtraService,Feedback

def home(request):
    return render(request, 'user/home.html')  # Render the home page.





   

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LaundryOrders, laundry_Membership

@login_required
def laundryorders(request):
    try:
        # Fetch user's active membership
        membership = laundry_Membership.objects.get(user=request.user)

        # Check if the membership is valid
        if membership.valid_until >= datetime.now().date():
            if request.method == 'POST':
                # Get form data
                clothes_count = request.POST.get('clothesCount')
                extra_item = request.POST.get('extras', '')
                check_in_date = request.POST.get('checkInDate')
                check_in_time = request.POST.get('checkInTime')

                # Validate clothes count
                if not clothes_count or not clothes_count.isdigit() or int(clothes_count) <= 0:
                    messages.error(request, "Please provide a valid number of clothes.")
                    return render(request, 'user/laundryorders.html')

                # Validate and parse check-in date and time
                try:
                    check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    messages.error(request, "Please provide a valid check-in date.")
                    return render(request, 'user/laundryorders.html')

                try:
                    check_in_time = datetime.strptime(check_in_time, "%H:%M").time()
                except (ValueError, TypeError):
                    messages.error(request, "Please provide a valid check-in time.")
                    return render(request, 'user/laundryorders.html')

                # Save the laundry order to the database
                LaundryOrders.objects.create(
                    user=request.user,
                    membership=membership,
                    clothes_count=int(clothes_count),
                    extra_item=extra_item,
                    check_in_date=check_in_date,
                    check_in_time=check_in_time,
                )

                # Success message and redirect
                messages.success(request, "Laundry order submitted successfully!")
                return redirect('home')

            # Render the form if the request is GET
            return render(request, 'user/laundryorders.html')

        else:
            # Redirect to membership renewal if expired
            messages.warning(request, "Your membership has expired. Please renew to place a laundry order.")
            return redirect('membership')

    except laundry_Membership.DoesNotExist:
        # Handle case where user has no membership
        messages.warning(request, "No active membership found. Please subscribe to a membership first.")
        return redirect('membership')

 








@login_required
def create_membership(request):
    # Check if the user has an existing membership
    existing_membership = laundry_Membership.objects.filter(user=request.user).first()
    
    if existing_membership:
        # Check if the existing membership has expired
        if existing_membership.valid_until >= date.today():
            return render(request, 'user/membership.html', {'error': 'You already have an active membership!'})
        else:
            # Membership has expired, so proceed with creating a new membership
            pass

    if request.method == 'POST':
        membership_type = request.POST.get('membership_type')
        payment_type = request.POST.get('payment_type')
        amount = request.POST.get('amount')

        if membership_type and payment_type:
            # Calculate the amount on the server to ensure security
            expected_amount = 3000 if membership_type == '6M' else 5000
            if int(amount) != expected_amount:
                return render(request, 'user/membership.html', {'error': 'Invalid amount!'})

            # Create payment and membership
            payment = laundry_Payments.objects.create(
                user=request.user,
                amount=expected_amount,
                payment_type=payment_type,
                payment_for='membership',
            )

            membership = laundry_Membership.objects.create(
                user=request.user,
                payment=payment,
                membership_type=membership_type,
                start_date=date.today(),
            )

            # Redirect to success page
            return redirect('home')

    return render(request, 'user/membership.html')










@login_required
def extra_service_view(request):
    if request.method == 'POST':
        # Get form data
        user = request.user  # Logged-in user
        extra_service_type = request.POST.get('extraService')  # Matches 'extraService' in model
        clothes_count = request.POST.get('clothesCount')  # Matches 'clothesCount' in model
        total_amount = request.POST.get('totalAmount') # Matches 'totalAmount' in model 
        payment_type = request.POST.get('paymentType')  # Matches 'paymentType' in model

        # Validate form data
        if not extra_service_type or not clothes_count or not payment_type:
            messages.error(request, "Please fill in all fields.")
            return redirect('extraservice')  # Redirect back to the form page

        try:
            clothes_count = int(clothes_count)
            if clothes_count <= 0:
                messages.error(request, "Clothes count must be greater than 0.")
                return redirect('extraservice')
        except ValueError:
            messages.error(request, "Invalid clothes count.")
            return redirect('extraservice')

        # Calculate the total amount based on the service type
        rates = {
            'dry_cleaning': 100,
            'ironing': 12,
            'folding': 3,
        }

        if extra_service_type not in rates:
            messages.error(request, "Invalid service type selected.")
            return redirect('extraservice')

        total_amount = clothes_count * rates[extra_service_type]  # Calculate the total amount

        # Save the extra service order to the database
        extra_service = ExtraService.objects.create(
            user=user,
            extraService=extra_service_type,
            clothesCount=clothes_count,
            totalAmount=total_amount,
            paymentType=payment_type
        )
        extra_service.save()

        # Success message and redirect
        messages.success(request, f"Order placed successfully! Total Amount: ₹{total_amount}")
        return redirect('extraservice')  # Redirect to the same page or another page

    # Render the form template
    return render(request, 'user/extraservice.html')





def payment(request):
    if request.method == 'POST':
        # Process the payment here
        # Redirect to the home page after payment
        return redirect('home')

    return render(request, 'user/payment.html')


from django.contrib.auth import logout

def user_logout(request):
    logout(request)  
    return redirect('login')








from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def feedback_view(request):
    if request.method == "POST":
        feedback_type = request.POST.get("feedbackType")
        message = request.POST.get("message")
        rating = request.POST.get("rating")

        if not feedback_type or not message or not rating:
            messages.error(request, "All fields are required.")
            return redirect("feedback")

        feedback = Feedback.objects.create(
            user=request.user,
            feedback_type=feedback_type,
            message=message,
            rating=int(rating),
        )
        messages.success(request, "Thank you for your feedback!")
        return redirect("feedback")

    return render(request, "user/feedback.html")
