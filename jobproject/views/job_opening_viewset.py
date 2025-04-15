from drf_queryfields import QueryFieldsMixin
from rest_framework import mixins, serializers, viewsets

from jobproject.models import JobOpening
from jobproject.services.permissions.DjangoModelPermissionsPlusGet import (
    DjangoModelPermissionsPlusGet,
)
from django_filters import rest_framework as filters


class _JobOpeningSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    include_arg_name = "include"
    exclude_arg_name = "exclude"
    delimiter = ","

    class Meta:
        model = JobOpening
        fields = ["id", "created", "applied", "active", "notes", "url", "company", "title", "location"]
        read_only_fields = ["created"]


class JobOpeningViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = JobOpening.objects.all()
    serializer_class = _JobOpeningSerializer
    permission_classes = [DjangoModelPermissionsPlusGet]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "active",
        "company",
        "title",
        "location",
    )
