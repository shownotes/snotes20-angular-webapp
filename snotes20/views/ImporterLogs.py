from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

import snotes20.models as models
import snotes20.serializers as serializers


class ImporterLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = models.ImporterLog.objects.order_by('starttime')[:3]
    serializer_class = serializers.ImporterLogSerializer
