from django.conf import settings
from django.db.models import Max

from rest_framework import viewsets
from rest_framework.response import Response

import snotes20.models as models
import snotes20.serializers as serializers

class ArchiveViewSet(viewsets.ViewSet):
    def list(self, request):
        qry = models.Podcast.objects.filter(episodes__publications__isnull=False)

        type = 'all'

        if 'type' in request.QUERY_PARAMS:
            type = request.QUERY_PARAMS['type']

        if type == 'recent':
            qry = qry.order_by('-episodes__publications__create_date')[:15]

        data = serializers.PodcastSerializer(qry, many=True).data

        return Response(data)
