from rest_framework import viewsets

from theatre.models import Actor
from theatre.serializers import ActorSerializer


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()
