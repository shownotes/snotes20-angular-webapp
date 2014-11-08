import datetime

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

import snotes20.models as models
import snotes20.serializers as serializers


class SoonEpisodeViewSet(viewsets.ViewSet):
    def list(self, request):
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = (today - datetime.timedelta(1))
        tomorrow = (today + datetime.timedelta(2))

        episodes = models.Episode.objects.filter(Q(date__lt=tomorrow) & (Q(date__gt=today) | Q(date__gt=yesterday) & Q(document__isnull=False)))\
                                 .order_by('date')[:10]

        return Response(serializers.EpisodeSerializer(episodes, many=True).data)
