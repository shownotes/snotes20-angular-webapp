import datetime

from django.conf import settings
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response

import snotes20.models as models
import snotes20.serializers as serializers




class MinimalEpisodeSerializer(serializers.BaseEpisodeSerializer):
    class Meta(serializers.BaseEpisodeSerializer.Meta):
        fields = ('id', 'number', 'date', 'type', 'create_date', 'stream', 'document')


class PrivateEpisodeViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.QUERY_PARAMS.get('secret', None) != settings.PRIVATE_API_SECRET:
            return Response([])

        episodes = models.Episode.objects.all()
        return Response(MinimalEpisodeSerializer(episodes, many=True).data)
