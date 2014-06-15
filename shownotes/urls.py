import datetime

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.db.transaction import atomic

from rest_framework import viewsets, routers, generics
from rest_framework.decorators import link
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed, APIException
from rest_framework.reverse import reverse

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
router.register(r'soonepisodes', SoonEpisodeViewSet, base_name='sonnepisode')
router.register(r'documents', DocumentViewSet, base_name='document')


class UnprocessableEntity(APIException):
    status_code = 422

    def __init__(self, detail):
        self.detail = detail


class DocumentByEpisodeViewSet(viewsets.ViewSet):
    def list(self, request):
        return 0

    def create(self, request, episode=None):
        doc = models.Document()
        ep = get_object_or_404(models.Episode.objects.filter(id=episode))

        if ep.document_id:
            raise UnprocessableEntity('this episode has a document')

        if 'name' not in request.DATA:
            raise UnprocessableEntity('no name supplied')

        name = request.DATA['name']

        if models.Document.objects.filter(name=name).exists():
            raise UnprocessableEntity('name taken')

        doc.name = name
        ep.document = doc

        with atomic():
            doc.save()
            ep.save()

        return Response(
            headers={'Location': reverse('document-detail', request=request, args=[name])},
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None, episode=None):
        doc = get_object_or_404(models.Document.objects.all().filter(episode=episode))
        return serializers.DocumentSerializer(doc)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


doc_by_ep_url = url('^documents/by-episode/(?P<episode>.+)/$',
                    DocumentByEpisodeViewSet.as_view({
                        'get': 'retrieve',
                        'post': 'create',
                    }))


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    doc_by_ep_url,
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
