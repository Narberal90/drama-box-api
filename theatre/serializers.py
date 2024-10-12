from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from theatre.models import Actor, Genre, Play, TheatreHall, Performance, Ticket, Reservation


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    actors = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "actors",
            "genres",
        )


class PlayRetrieveSerializer(PlaySerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "show_time", "play", "theatre_hall")


class PerformanceListSerializer(PerformanceSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    theatre_hall_capacity = serializers.IntegerField(
        source="theatre_hall.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "play_title",
            "show_time",
            "theatre_hall_name",
            "theatre_hall_capacity",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, data: dict) -> dict:
        Ticket.validate_ticket_position(
            data["row"], data["seat"], data["performance"].theatre_hall
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(many=False, read_only=True)


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayRetrieveSerializer(many=False, read_only=True)
    theatre_hall = TheatreHallSerializer(many=False, read_only=True)
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = Performance
        fields = ("id", "show_time", "play", "theatre_hall", "taken_places")


class PerformanceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = (
            "play",
            "theatre_hall",
            "show_time",
        )


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
