from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_reservation_confirmation_email(reservation_id, user_email):
    subject = "Reservation Confirmation"
    message = (
        f"Your reservation has been confirmed. "
        f"Reservation ID: {reservation_id}"
    )
    recipient_list = [user_email]

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
