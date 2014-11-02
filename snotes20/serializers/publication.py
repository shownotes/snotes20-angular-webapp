from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from snotes20.models import Publication, PublicationRequest
from snotes20.serializers import EpisodeSerializer



class PublicationSerializer(ModelSerializer):

    class Meta:
        model = Publication
        fields = ('order', 'message', 'date', 'issuer', 'document')
