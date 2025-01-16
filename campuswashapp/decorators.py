from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps

def membership_required(view_func):
    @wraps(view_func)
    @login_required  # Ensure the user is logged in first
    def wrapper(request, *args, **kwargs):
        # Check if the user has a profile and membership
        if not hasattr(request.user, 'profile') or not request.user.profile.has_membership:
            messages.info(request, "Please take the membership to place orders.")
            return redirect('membership')  # Replace with the actual URL name for the membership page
        return view_func(request, *args, **kwargs)
    return wrapper
