from rest_framework.serializers import ModelSerializer

from snotes20.models import Podcast, Episode


class PodcastSerializer(ModelSerializer):
    class Meta:
        model = Podcast
        fields = ('id', 'slug', 'creator', 'title', 'description', 'url', 'stream', 'chat',
                  'type', 'deleted', 'approved', 'create_date')


class EpisodeSerializer(ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'podcast', 'creator', 'number', 'episodeurl', 'date', 'canceled',
                  'type', 'create_date', 'stream', 'document')