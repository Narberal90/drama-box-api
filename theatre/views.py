from rest_framework import viewsets

from theatre.models import Actor, Genre
from theatre.serializers import ActorSerializer, GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class GenreViewSet(viewsets.ModelViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
