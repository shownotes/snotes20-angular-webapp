import datetime

from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import snotes20.models as models
import snotes20.serializers as serializers


class SoonEpisodeViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        today =  datetime.date.today()
        yesterday = (today - datetime.timedelta(1))

        episodes = models.Episode.objects.filter(date__gt=yesterday)\
                                 .filter(date__lt=today)\
                                 .order_by('date')[:10]

        return Response(serializers.EpisodeSerializer(episodes).data)

    def retrieve(self, request, pk=None):
        raise MethodNotAllowed('GET')