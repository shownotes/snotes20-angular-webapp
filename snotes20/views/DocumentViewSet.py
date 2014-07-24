from datetime import datetime

from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

import snotes20.serializers as serializers
import snotes20.models as models

def create_doc_from_episode(request):
    if 'episode' not in request.DATA:
        raise PermissionDenied()
    if not request.user.is_authenticated():
        raise PermissionDenied()

    episode = get_object_or_404(models.Episode, pk=request.DATA['episode'])

    today = datetime.now()

    doc = models.Document()

    doc.name = episode.podcast.slug + '-' + today.strftime('%Y-%m-%d-%H-%M-%S')
    doc.editor = models.EDITOR_ETHERPAD
    doc.creator = request.user

    with transaction.atomic():
        doc.save()
        episode.document = doc
        episode.save()

    return Response({'name': doc.name}, status=status.HTTP_201_CREATED)


def get_doc_impl(document):
    if document is not None:
        data = serializers.DocumentSerializer(instance=document)
        return Response(data.data)
    else:
        return Response(None, status=status.HTTP_404_NOT_FOUND)


def get_doc_by_episode(request, pk=None):
    number = request.QUERY_PARAMS['number']
    podcast = request.QUERY_PARAMS['podcast']

    episode = get_object_or_404(models.Episode, number=number, podcast__slugs__slug=podcast)

    return get_doc_impl(episode.document)


def get_doc(request, pk=None):
    return get_doc_impl(get_object_or_404(models.Document, pk=pk))


class DocumentViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        type = request.QUERY_PARAMS.get('type')

        if type == 'fromepisode':
            return create_doc_from_episode(request)
        else:
            raise PermissionDenied()

    def retrieve(self, request, pk=None):
        type = request.QUERY_PARAMS.get('type')

        if type == 'byepisode':
            return get_doc_by_episode(request)
        else:
            return get_doc(request, pk)

    #def list(self, request):
    #    pass

    #def update(self, request, pk=None):
    #    pass

    #def partial_update(self, request, pk=None):
    #    pass

    #def destroy(self, request, pk=None):
    #    pass