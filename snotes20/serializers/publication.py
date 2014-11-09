from rest_framework.serializers import ModelSerializer

from snotes20.models import Publication, PublicationRequest


class PublicationSerializer(ModelSerializer):

    class Meta:
        model = Publication
        fields = ('id', 'create_date', 'shownoters', 'podcasters', 'preliminary', 'comment')


class PublicationRequestSerializer(ModelSerializer):

    class Meta:
        model = PublicationRequest
        fields = ('id', 'create_date', 'shownoters', 'podcasters', 'preliminary', 'comment')
