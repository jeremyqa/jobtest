from rest_framework import mixins, serializers, viewsets

from jobproject.models import JobOpening
from jobproject.services.permissions.DjangoModelPermissionsPlusGet import (
    DjangoModelPermissionsPlusGet,
)


class _JobOpeningSerializer(serializers.Serializer):
    created = serializers.DateTimeField(read_only=True)
    applied = serializers.DateTimeField()
    active = serializers.BooleanField()
    notes = serializers.CharField()
    url = serializers.CharField()
    company = serializers.CharField()
    title = serializers.CharField()
    location = serializers.CharField()


class JobOpeningViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = JobOpening.objects.all()
    serializer_class = _JobOpeningSerializer
    permission_classes = [DjangoModelPermissionsPlusGet]
