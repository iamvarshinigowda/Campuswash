from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.conf import settings

def send_status_update_email(user_email, order_id):
    subject = "Your Laundry Order is Ready!"
    message = f"Dear Customer,\n\nYour laundry order with ID {order_id} is now ready for collection.\n\nThank you for using our service!"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    try:
        send_mail(subject, message, email_from, recipient_list)
        print(f"Email sent to {user_email}")
    except BadHeaderError:
        print("Invalid header found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
