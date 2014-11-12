from rest_framework.serializers import ModelSerializer, Field

from snotes20.models import Podcast, Episode

from .cover import CoverSerializer


class BaseEpisodeSerializer(ModelSerializer):

    class Meta:
        model = Episode
        fields = ('id', 'creator', 'number', 'episode_url', 'date', 'canceled', 'type',
                  'create_date', 'stream', 'publications', 'publicationrequests', 'document', 'podcast')
        depth = 1

class BasePodcastSerializer(ModelSerializer):
    slug = Field()
    num_episodes = Field()

    class Meta:
        model = Podcast
        fields = ('id', 'slug', 'creator', 'title', 'description', 'url', 'stream', 'chat',
                  'type', 'deleted', 'approved', 'create_date', 'num_episodes', 'episodes')


class SubPodcastSerializer(BasePodcastSerializer):
    class Meta(BasePodcastSerializer.Meta):
        fields = list(set(BasePodcastSerializer.Meta.fields) - {'episodes',})

class EpisodeSerializer(BaseEpisodeSerializer):
    podcast = SubPodcastSerializer()



class SubEpisodeSerializer(BaseEpisodeSerializer):
    class Meta(BaseEpisodeSerializer.Meta):
        fields = list(set(BaseEpisodeSerializer.Meta.fields) - {'podcast',})

class PodcastSerializer(ModelSerializer):
    episodes = SubEpisodeSerializer(many=True)
