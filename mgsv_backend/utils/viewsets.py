from functools import wraps, reduce

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets


def extended_route(serializer: serializers.ModelSerializer):
    def decorator(function):
        @wraps(function)
        def wrapper(viewset: viewsets.ModelViewSet, request, *args, **kwargs):
            original_serializer = viewset.serializer_class
            if (
                "extended" in request.query_params
                and request.query_params["extended"][0] == "1"
            ):
                viewset.serializer_class = serializer

            result = function(viewset, request, *args, **kwargs)
            viewset.serializer_class = original_serializer
            return result

        return wrapper

    return decorator


def extended_route_self():
    def decorator(function):
        @wraps(function)
        def wrapper(viewset, request, *args, **kwargs):
            original_serializer = viewset.serializer_class
            if (
                "extended" in request.query_params
                and request.query_params["extended"][0] == "1"
            ):
                viewset.serializer_class = viewset.extended_serializer_class

            result = function(viewset, request, *args, **kwargs)
            viewset.serializer_class = original_serializer
            return result

        return wrapper

    return decorator


class ExtendedViewSetMixin:
    extended_serializer_class: serializers.ModelSerializer = None

    @extended_route_self()
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @extended_route_self()
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class MultipleFieldLookupMixin:
    lookup_fields = ("pk",)
    lookup_ignorecase = True

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {
            "{}{}".format(
                field, "__iexact" if self.lookup_ignorecase else ""
            ): self.kwargs[self.lookup_field]
            for field in self.lookup_fields
        }

        obj = get_object_or_404(
            queryset, reduce(lambda x, y: Q(x) | Q(y), filter.items())
        )
        self.check_object_permissions(self.request, obj)
        return obj
