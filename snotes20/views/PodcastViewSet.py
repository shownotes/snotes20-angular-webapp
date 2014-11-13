from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

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

    @action(methods=["GET"])
    def covers(self, request, pk=None):
        podcast = get_object_or_404(models.Podcast, slugs__slug=pk)

        covers = []

        try:
            covers.append(podcast.cover)
        except models.Cover.DoesNotExist:
            pass

        ep_covers = models.Cover.objects.filter(episodes__podcast=podcast).distinct()

        if len(covers) > 0:
            ep_covers = ep_covers.exclude(id=covers[0].id)

        covers.extend(ep_covers)

        data = serializers.CoverSerializer(covers, many=True).data

        return Response(data)