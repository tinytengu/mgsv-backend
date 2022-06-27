from rest_framework import viewsets

from mgsv_backend.utils.viewsets import ExtendedViewSetMixin, MultipleFieldLookupMixin
from .models import *
from .serializers import *


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


class DialogViewSet(viewsets.ModelViewSet):
    serializer_class = DialogSerializer
    queryset = Dialog.objects.all()
