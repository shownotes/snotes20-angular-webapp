from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from snotes20.models import Document


class DocumentSerializer(ModelSerializer):
    episode = PrimaryKeyRelatedField(required=False)

    class Meta:
        model = Document
        fields = ('name', 'editor', 'create_date', 'creator', 'episode')
