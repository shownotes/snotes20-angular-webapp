from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response

import snotes20.models as models
import snotes20.serializers as serializers

class ArchiveViewSet(viewsets.ViewSet):
    def list(self, request):
        pods = models.Podcast.objects.all()

        data = serializers.PodcastSerializer(pods, many=True).data

        return Response(data)
