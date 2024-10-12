from django.db.models import F, Count
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from theatre.filters import PlayFilter, PerformanceFilter
from theatre.models import Actor, Genre, Play, TheatreHall, Performance, Reservation
from theatre.ordering import PerformanceOrdering
from theatre.permissions import IsAdminOrIfAuthenticatedReadOnly, IsAdminOrIfAnonReadOnly
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    TheatreHallSerializer,
    PerformanceSerializer, PerformanceListSerializer, PerformanceDetailSerializer, ReservationSerializer,
    ReservationListSerializer, PerformanceCreateUpdateSerializer, PlayRetrieveSerializer, PlayImageSerializer
)
from django.utils.timezone import now


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminUser,)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("genres", "actors")
    serializer_class = PlaySerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PlayFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            queryset = queryset.filter(
                performances__show_time__gte=now()
            ).distinct()

            if self.request.user.is_authenticated:
                queryset = queryset | Play.objects.filter(
                    performances__tickets__reservation__user=self.request.user
                ).distinct()

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayRetrieveSerializer
        if self.action == "upload-image":
            return PlayImageSerializer

        return self.serializer_class

    @action(
        methods=["POST", "PUT", "PATCH"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading or updating image for a specific play."""
        play = self.get_object()
        serializer = self.get_serializer(play, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerformanceViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceSerializer
    permission_classes = (IsAdminOrIfAnonReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PerformanceFilter
    queryset = (
        Performance.objects.all()
        .select_related("play", "theatre_hall")
        .annotate(
            tickets_available=(
                F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
                - Count("tickets")
            )
        )
    )

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        if self.action in ["create", "update", "partial_update"]:
            return PerformanceCreateUpdateSerializer
        return super().get_serializer_class()

    def get_ordering(self):
        fields = ["show_time", "play__title", "theatre_hall__name", "tickets_available"]
        return PerformanceOrdering.get_ordering_fields(self.request, fields)

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.get_ordering()
        return queryset.order_by(*ordering)


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Reservation.objects.prefetch_related(
        "tickets__performance__play", "tickets__performance__theatre_hall"
    )
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
