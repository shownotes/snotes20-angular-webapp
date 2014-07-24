from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from snotes20.models import Document
from snotes20.serializers import EpisodeSerializer


class DocumentSerializer(ModelSerializer):
    episode = EpisodeSerializer()

    class Meta:
        model = Document
        fields = ('name', 'editor', 'create_date', 'episode')
