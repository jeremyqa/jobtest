from rest_framework import viewsets, mixins, serializers
from jobproject.models import JobOpening
from rest_framework.permissions import DjangoModelPermissions


class _JobOpeningSerializer(serializers.Serializer):
    created = serializers.DateTimeField(read_only=True)
    applied = serializers.BooleanField()
    active = serializers.BooleanField()
    notes = serializers.CharField()
    url = serializers.CharField()
    company = serializers.CharField()
    title = serializers.CharField()
    location = serializers.CharField()


class JobOpeningViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = JobOpening.objects.all()
    serializer_class = _JobOpeningSerializer
    permission_classes = [DjangoModelPermissions]
