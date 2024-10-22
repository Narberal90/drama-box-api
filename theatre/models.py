import os
import uuid

from django.contrib.auth import get_user_model
from django.utils.text import slugify

from django.db import models
from django.core.exceptions import ValidationError


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


def play_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/plays/", filename)


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="plays")
    image = models.ImageField(null=True, upload_to=play_image_file_path)

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.play.title} at {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reservations"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Reservation made on "
            f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ("seat",)

    def __str__(self):
        return f"Row {self.row}, Seat {self.seat} for {self.performance}"

    @staticmethod
    def validate_ticket_position(
        row: int, seat: int, theatre_hall: TheatreHall
    ) -> None:
        max_rows = theatre_hall.rows
        if not (1 <= row <= max_rows):
            raise ValidationError(
                {
                    "row": f"Row number must be in available range: "
                           f"(1, {max_rows})"
                }
            )

        max_seats_in_row = theatre_hall.seats_in_row
        if not (1 <= seat <= max_seats_in_row):
            raise ValidationError(
                {
                    "seat": f"Seat number must be in available range: "
                            f"(1, {max_seats_in_row})"
                }
            )

    def clean(self):
        self.validate_ticket_position(
            self.row, self.seat, self.performance.theatre_hall
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
