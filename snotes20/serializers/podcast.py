from rest_framework.serializers import ModelSerializer, Field

from snotes20.models import Podcast, Episode

from .cover import CoverSerializer


class BaseEpisodeSerializer(ModelSerializer):
    cover = CoverSerializer()

    class Meta:
        model = Episode
        fields = ('id', 'creator', 'number', 'episode_url', 'date', 'canceled', 'type', 'cover',
                  'create_date', 'stream', 'publications', 'publicationrequests', 'document', 'podcast')
        depth = 1

class BasePodcastSerializer(ModelSerializer):
    slug = Field()
    num_episodes = Field()
    cover = CoverSerializer()

    class Meta:
        model = Podcast
        fields = ('id', 'slug', 'creator', 'title', 'description', 'url', 'stream', 'chat', 'cover',
                  'type', 'deleted', 'approved', 'create_date', 'num_episodes', 'episodes')


class SubPodcastSerializer(BasePodcastSerializer):
    class Meta(BasePodcastSerializer.Meta):
        fields = list(set(BasePodcastSerializer.Meta.fields) - {'episodes',})

class EpisodeSerializer(BaseEpisodeSerializer):
    podcast = SubPodcastSerializer()



class SubEpisodeSerializer(BaseEpisodeSerializer):
    class Meta(BaseEpisodeSerializer.Meta):
        fields = list(set(BaseEpisodeSerializer.Meta.fields) - {'podcast',})

class PodcastSerializer(BasePodcastSerializer):
    episodes = SubEpisodeSerializer(many=True)
