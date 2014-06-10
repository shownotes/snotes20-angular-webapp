import datetime

from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import viewsets, routers
from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed


import snotes20.models as models
import snotes20.serializers as serializers


class SoonEpisodeViewSet(viewsets.ViewSet):

    def list(self, request):
        today =  datetime.date.today()
        yesterday = (today - datetime.timedelta(1))

        episodes = models.Episode.objects.filter(date__gt=yesterday)\
                                 .filter(date__lt=today)\
                                 .order_by('date')[:10]

        return Response(serializers.EpisodeSerializer(episodes).data)

    def retrieve(self, request, pk=None):
        raise MethodNotAllowed('GET')


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')


router = routers.DefaultRouter()
router.register(r'soonepisodes', SoonEpisodeViewSet, base_name='sonnepisodes')
router.register(r'documents', DocumentViewSet, base_name='documents')



urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
