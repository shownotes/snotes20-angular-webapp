from django.conf import settings
from django.db.models import Max, Q
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, list_route

import snotes20.models as models
import snotes20.serializers as serializers

class ArchiveViewSet(viewsets.ViewSet):
    def list(self, request):
        type = 'all'

        if 'type' in request.QUERY_PARAMS:
            type = request.QUERY_PARAMS['type']

        if type == 'recent':
            qry = models.Podcast.objects.raw(
                'SELECT DISTINCT ON ("id", pub_create) * '
                'FROM ('
                '  SELECT "snotes20_podcast".*, snotes20_publication.create_date AS pub_create'
                '  FROM "snotes20_podcast"'
                '  INNER JOIN "snotes20_episode" ON ("snotes20_podcast"."id" = "snotes20_episode"."podcast_id")'
                '  INNER JOIN "snotes20_publication" ON ("snotes20_episode"."id" = "snotes20_publication"."episode_id")'
                '  WHERE "snotes20_publication"."id" IS NOT NULL'
                ') AS subb '
                'ORDER BY pub_create DESC '
                'LIMIT ' + str(settings.ARCHIVE_RECENT_COUNT) + ';'
            )
        elif type == 'full':
            qry = models.Podcast.objects.all()
        else:
            qry = models.Podcast.objects.raw(
                'SELECT DISTINCT ON ("id", "title") * '
                'FROM ('
                '  SELECT "snotes20_podcast".*'
                '  FROM "snotes20_podcast"'
                '  INNER JOIN "snotes20_episode" ON ("snotes20_podcast"."id" = "snotes20_episode"."podcast_id")'
                '  INNER JOIN "snotes20_publication" ON ("snotes20_episode"."id" = "snotes20_publication"."episode_id")'
                '  WHERE "snotes20_publication"."id" IS NOT NULL'
                ') AS subb '
                'ORDER BY title, id;'
            )

        data = serializers.MinimalPodcastSerializer(qry, many=True).data

        return Response(data)

    @list_route(methods=['POST'])
    def search(self, request):
        words = request.DATA['words']
        lines = models.OSFNote.objects.filter(Q(title__icontains=words) or Q(url__icontains=words))\
                                      .filter(state__publication__isnull=False)\
                                      .distinct('state__publication__episode')

        lines = lines[:15]

        data = [
            {
                'note': serializers.OSFNoteSerializer(line).data,
                'episode': serializers.EpisodeSerializer(line.state.publication.episode).data,
            } for line in lines
        ]

        return Response(data)
