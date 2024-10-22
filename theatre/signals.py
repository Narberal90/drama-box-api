from django.db.models.signals import post_save
from django.dispatch import receiver
from theatre.models import Reservation
from theatre.tasks import send_reservation_confirmation_email


@receiver(post_save, sender=Reservation)
def send_reservation_confirmation(sender, instance, created, **kwargs):
    if created:
        send_reservation_confirmation_email.delay(
            instance.id, instance.user.email
        )
