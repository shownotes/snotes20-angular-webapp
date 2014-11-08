from datetime import datetime
import time

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

import snotes20.serializers as serializers
import snotes20.models as models
import snotes20.editors as editors

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

    meta = models.DocumentMeta()

    with transaction.atomic():
        meta.save()
        doc.meta = meta

        doc.save()

        episode.document = doc
        episode.save()

    return Response({'name': doc.name}, status=status.HTTP_201_CREATED)


def get_doc_impl(document):
    if document is not None:
        data = serializers.DocumentSerializer(instance=document)
        return document, Response(data.data)
    else:
        return None, Response(None, status=status.HTTP_404_NOT_FOUND)


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
            doc, resp = get_doc_by_episode(request)
        else:
            doc, resp = get_doc(request, pk)

        if resp.status_code == 200 and request.user.is_authenticated():
            editor = editors.EditorFactory.get_editor(doc.editor)
            urlname = editor.get_urlname_for_document(doc)

            resp.data['urlname'] = urlname

            session_id = editor.generate_session(doc, request.user)
            resp.set_cookie('sessionID', session_id)

        return resp

    @action(methods=['POST', 'DELETE'])
    def contributed(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)
        exists = any(noter.username == request.user.username for noter in document.meta.shownoters.all())

        if request.method == 'POST' and not exists:
            document.meta.shownoters.add(request.user)
        elif request.method == 'DELETE' and exists:
            document.meta.shownoters.remove(request.user)

        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST', 'DELETE'])
    def podcasters(self, request, pk=None):
        if 'name' not in request.DATA:
            raise PermissionDenied()

        name = request.DATA['name']
        document = get_object_or_404(models.Document, pk=pk)
        exists = any(rpodcaster.name == name for rpodcaster in document.meta.podcasters.all())

        if request.method == 'POST' and not exists:
            rpodcaster = models.RawPodcaster(name=name)
            try:
                rpodcaster.clean_fields()
            except ValidationError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            document.meta.podcasters.add(rpodcaster)
        elif request.method == 'DELETE' and exists:
            document.meta.podcasters.get(name=name).delete()

        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST', 'GET'])
    def chat(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)

        if request.method == 'POST':
            if 'message' not in request.DATA:
                raise PermissionDenied()

            issuer = models.ChatMessageIssuer()
            issuer.type = models.CHAT_MSG_ISSUER_USER
            issuer.user = request.user
            issuer.save()

            msg = models.ChatMessage()
            msg.message = request.DATA['message']
            msg.document = document
            msg.issuer = issuer
            msg.order = int(round(time.time() * 1000))
            msg.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        elif request.method == 'GET':
            msgs = document.messages.all()

            try:
                if 'since' in request.QUERY_PARAMS:
                    msgs = msgs.filter(order__gt=int(request.QUERY_PARAMS['since']))
            except:
                return Response([], status=status.HTTP_200_OK)

            data = serializers.ChatMessageSerializer(msgs).data
            return Response(data, status=status.HTTP_200_OK)

    @action(methods=['POST'])
    def text(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)

        type = 'osf'

        if 'type' in request.QUERY_PARAMS:
            type = request.QUERY_PARAMS['type']

        if type == 'json':
            try:
                data = document.state.osfdocumentstate.to_dict()
            except models.OSFDocumentState.DoesNotExist:
                raise PermissionDenied()
        elif type == 'raw':
            data  = document.raw_state.text
        elif type == 'osf':
            data = None
        else:
            raise PermissionDenied()

        response = Response({'data': data}, status=status.HTTP_200_OK)
        return response

    @action(methods=['GET'])
    def errors(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)
        errors = document.state.errors.all()
        return Response(serializers.DocumentStateErrorSerializer(errors).data, status=status.HTTP_200_OK)


    @action(methods=['POST', 'GET'])
    def publications(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)

        if not hasattr(document, 'episode'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        episode = document.episode

        if request.method == 'POST':

            return Response(status=status.HTTP_202_ACCEPTED)
        elif request.method == 'GET':
            return Response(episode.publications)


    @action(methods=['GET'])
    def canpublish(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)

        if not hasattr(document, 'episode'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        episode = document.episode

        if not request.user.is_authenticated() or not request.user.has_perm('o_publish_episode', episode):
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_200_OK)

    #def list(self, request):
    #    pass

    #def update(self, request, pk=None):
    #    pass

    #def partial_update(self, request, pk=None):
    #    pass

    #def destroy(self, request, pk=None):
    #    pass