from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

import snotes20.models as models
import snotes20.serializers as serializers


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')