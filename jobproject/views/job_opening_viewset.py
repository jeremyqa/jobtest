from django_filters import OrderingFilter
from django_filters import rest_framework as filters
from drf_queryfields import QueryFieldsMixin
from rest_framework import mixins, serializers, viewsets

from jobproject.models import JobOpening
from jobproject.services.permissions.DjangoModelPermissionsPlusGet import (
    DjangoModelPermissionsPlusGet,
)


class _JobOpeningFilter(filters.FilterSet):
    # https://django-filter.readthedocs.io/en/stable/ref/filters.html#orderingfilter
    # https://stackoverflow.com/questions/33691933/how-can-i-use-orderingfilter-without-exposing-the-names-of-the-fields-in-the-dat
    ordering = OrderingFilter(fields=(("id", "id"), ("applied", "applied"), ("status", "status")))

    class Meta:
        model = JobOpening
        fields = (
            "active",
            "company",
            "title",
            "location",
            "status",
        )


class _JobOpeningSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    include_arg_name = "include"
    exclude_arg_name = "exclude"
    delimiter = ","

    class Meta:
        model = JobOpening
        fields = ["id", "created", "applied", "active", "notes", "url", "company", "title", "location", "status"]
        read_only_fields = ["created"]


class JobOpeningViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = JobOpening.objects.all()
    serializer_class = _JobOpeningSerializer
    permission_classes = [DjangoModelPermissionsPlusGet]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = _JobOpeningFilter
