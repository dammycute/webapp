from celery import shared_task
from django.core.mail import send_mail
from .models import NinModel
from authApp.models import CustomUser
# import request

def send_nin_verification_success_notification(user, transaction_id):
    subject = "NIN Verification Successful"
    message = f"Your NIN verification for transaction ID {transaction_id} has been completed successfully."
    send_mail(subject, message, 'noreply@example.com', [user.email])

def send_nin_verification_failure_notification(user, transaction_id):
    subject = "NIN Verification Failed"
    message = f"Your NIN verification for transaction ID {transaction_id} has failed."
    send_mail(subject, message, 'noreply@example.com', [user.email])
