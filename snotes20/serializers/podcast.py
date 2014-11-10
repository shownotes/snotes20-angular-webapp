from rest_framework.serializers import ModelSerializer, Field

from snotes20.models import Podcast, Episode


class EpisodeSerializer(ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'podcast', 'creator', 'number', 'episode_url', 'date', 'canceled', 'type',
                  'create_date', 'stream', 'publications', 'publicationrequests', 'document')
        depth = 1


class PodcastSerializer(ModelSerializer):
    slug = Field()
    num_episodes = Field()
    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = Podcast
        fields = ('id', 'slug', 'creator', 'title', 'description', 'url', 'stream', 'chat',
                  'type', 'deleted', 'approved', 'create_date', 'num_episodes', 'episodes')
