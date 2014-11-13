from rest_framework.serializers import ModelSerializer

from snotes20.models import Publication, PublicationRequest


class PublicationSerializer(ModelSerializer):

    class Meta:
        model = Publication
        read_only_fields = ('shownoters', 'podcasters')
        fields = ('id', 'create_date', 'shownoters', 'podcasters', 'preliminary', 'comment')


class PublicationRequestSerializer(ModelSerializer):

    class Meta:
        model = PublicationRequest
        read_only_fields = ('shownoters', 'podcasters')
        fields = ('id', 'create_date', 'shownoters', 'podcasters', 'preliminary', 'comment')
