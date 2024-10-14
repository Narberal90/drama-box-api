from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Reservation


@receiver(post_save, sender=Reservation)
def send_reservation_confirmation(sender, instance, created, **kwargs):
    if created:
        subject = 'Reservation Confirmation'
        message = f'Your reservation has been confirmed. Reservation ID: {instance.id}'
        recipient_list = [instance.user.email]

        send_mail(subject, message, EMAIL_HOST_USER, recipient_list)
