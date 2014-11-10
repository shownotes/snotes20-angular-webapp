from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response

import snotes20.models as models
import snotes20.serializers as serializers

class PodcastViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            pod = models.Podcast.objects.get(slugs__slug=pk)
        except models.Podcast.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = serializers.PodcastSerializer(pod).data
        return Response(data)
