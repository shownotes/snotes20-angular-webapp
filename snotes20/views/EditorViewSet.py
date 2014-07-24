from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response

import snotes20.models as models

class EditorViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([
            {
                'short': short,
                'long': long,
                'url': settings.EDITORS[short]['userurl']
            } for short, long in models.EDITOR_CHOICES
        ])
