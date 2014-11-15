from datetime import datetime
import time

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q, Count
from django.core.validators import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action, list_route

import snotes20.serializers as serializers
import snotes20.models as models
import snotes20.editors as editors
import snotes20.contenttypes as contenttypes

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
        data = serializers.DocumentSerializer(instance=document).data
        return document, Response(data)
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

        if resp.status_code == 200 and request.user.is_authenticated() and 'edit' in request.QUERY_PARAMS:
            editor = editors.EditorFactory.get_editor(doc.editor)
            session_id = editor.generate_session(doc, request.user)
            resp.set_cookie('sessionID', session_id)

            doc.edit_date = datetime.now()

        doc.access_date = datetime.now()
        doc.save(update_fields=['edit_date', 'access_date'])

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

    @action(methods=['POST'])
    def number(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)

        if not hasattr(document, 'episode'):
            return Response(status=status.HTTP_404_NOT_FOUND)

        episode = document.episode

        if episode.number is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            episode.number = int(request.DATA['number'])
            episode.full_clean()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        episode.save()

        return Response(status=status.HTTP_202_ACCEPTED)

    @list_route()
    def todo(self, request):
        if not request.user.has_perm('snotes20.publish_episode') and not models.Podcast.objects.filter(mums=request.user).exists():
            raise PermissionDenied()

        qry = models.Document.objects.filter(episode__isnull=False)\
                                     .annotate(Count('episode__publications'))\
                                     .annotate(Count('episode__publicationrequests'))\
                                     .filter(Q(episode__publications__count=0) |
                                             Q(episode__publicationrequests__count__gt=0))

        if 'search' in request.QUERY_PARAMS:
            key = request.QUERY_PARAMS['search']
            qry = qry.filter(episode__podcast__title__icontains=key)

        return Response({
            'data': serializers.DocumentSerializer(qry[:15], many=True).data,
            'count': qry.count()
        })

    @action(methods=['POST', 'DELETE'])
    def shownoters(self, request, pk=None):
        if 'name' not in request.DATA and 'id' not in request.DATA:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        document = get_object_or_404(models.Document, pk=pk)

        if not hasattr(document, 'episode'):
            return Response(status=status.HTTP_404_NOT_FOUND)

        episode = document.episode

        if not request.user.has_perm('o_publish_episode', episode):
            raise PermissionDenied()

        try:
            if 'name' in request.DATA:
                shownoter = models.NUser.objects.get(username=request.DATA['name'])
            else:
                shownoter = models.NUser.objects.get(id=request.DATA['id'])
        except models.NUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'DELETE':
            document.meta.shownoters.remove(shownoter)
        elif request.method == 'POST':
            document.meta.shownoters.add(shownoter)

        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST', 'DELETE'])
    def podcasters(self, request, pk=None):
        if 'name' not in request.DATA:
            raise PermissionDenied()

        name = request.DATA['name']
        document = get_object_or_404(models.Document, pk=pk)
        exists = any(rpodcaster.name == name for rpodcaster in document.meta.podcasters.all())

        if request.method == 'POST' and not exists:
            rpodcaster = models.RawPodcaster(name=name, meta=document.meta)
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

            data = serializers.ChatMessageSerializer(msgs, many=True).data
            return Response(data, status=status.HTTP_200_OK)

    @action(methods=['POST'])
    def text(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)

        type = 'osf'

        source = document

        if 'type' in request.QUERY_PARAMS:
            type = request.QUERY_PARAMS['type']

        if 'pub' in request.QUERY_PARAMS:
            try:
                num = int(request.QUERY_PARAMS['pub'])
                source = document.episode.publications.order_by('create_date')[num:num + 1][0]
            except IndexError:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if type == 'json':
            try:
                data = source.state.osfdocumentstate.to_dict()
            except models.OSFDocumentState.DoesNotExist:
                raise PermissionDenied()
        elif type == 'raw':
            data  = source.raw_state.text
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
        data = serializers.DocumentStateErrorSerializer(errors, many=True).data
        return Response(data, status=status.HTTP_200_OK)


    @action(methods=['POST', 'GET'])
    def publications(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)

        if not hasattr(document, 'episode'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        episode = document.episode

        if request.method == 'POST':
            if not request.user.is_authenticated() or not request.user.has_perm('o_publish_episode', episode):
                return Response(status=status.HTTP_403_FORBIDDEN)

            podcasters = request.DATA['podcasters']
            request.DATA['podcasters'] = []

            cover = None
            if 'cover' in request.DATA:
                cover = request.DATA['cover']
                del request.DATA['cover']

            request.DATA['create_date'] = datetime.now()

            serialized = serializers.PublicationSerializer(data=request.DATA)

            if not serialized.is_valid():
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

            pub = serialized.object

            with transaction.atomic():
                raw_state, state = contenttypes.get_state(document)
                state.save()

                if cover is not None:
                    if cover['id'] == 'new':
                        cover = models.Cover.from_url(request.user, cover['file'])
                    else:
                        cover = models.Cover.objects.get(pk=cover['id'])

                    episode.cover = cover
                    episode.save()

                pub.creator = request.user
                pub.state = state
                pub.raw_state = raw_state
                pub.episode = episode

                pub.save()

                pub.shownoters.add(*document.meta.shownoters.all())

                episode.publicationrequests.all().delete()

            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'GET':
            return Response(episode.publications)

    @action(methods=['POST'])
    def publicationrequests(self, request, pk=None):
        document = get_object_or_404(models.Document, pk=pk)

        if not hasattr(document, 'episode'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        episode = document.episode

        if episode.publicationrequests.count() != 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        comment = ""

        if 'comment' in request.DATA:
            comment = request.DATA['comment']

        request = models.PublicationRequest(episode=episode,
                                            comment=comment,
                                            requester=request.user,
                                            create_date=datetime.now())
        try:
            request.clean_fields()
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request.save()

        return Response(status=status.HTTP_201_CREATED)

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