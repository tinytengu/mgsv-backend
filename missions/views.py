from rest_framework import viewsets

from mgsv_backend.utils.viewsets import ExtendedViewSetMixin, MultipleFieldLookupMixin
from .models import *
from .serializers import *


class CharacterViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()
    lookup_fields = ("pk", "slug")


class MissionViewSet(
    ExtendedViewSetMixin, MultipleFieldLookupMixin, viewsets.ModelViewSet
):
    serializer_class = MissionSerializer
    extended_serializer_class = MissionSerializerExtended
    queryset = Mission.objects.all()
    lookup_fields = ("pk", "slug")


class ObjectiveViewSet(ExtendedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ObjectiveSerializer
    extended_serializer_class = ObjectiveSerializerExtended
    queryset = Objective.objects.all()


class FactViewSet(viewsets.ModelViewSet):
    serializer_class = FactSerializer
    queryset = Fact.objects.all()


class DialogViewSet(ExtendedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = DialogSerializer
    extended_serializer_class = DialogSerializerExtended
    queryset = Dialog.objects.all()
