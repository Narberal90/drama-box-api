from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from theatre.filters import PlayFilter
from theatre.models import Actor, Genre, Play, TheatreHall, Performance
from theatre.permissions import IsAdminOrIfAuthenticatedReadOnly
from theatre.serializers import ActorSerializer, GenreSerializer, PlaySerializer, TheatreHallSerializer, \
    PerformanceSerializer
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


