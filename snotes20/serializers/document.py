from rest_framework.serializers import ModelSerializer

from snotes20.models import Document


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'editor', 'create_date', 'creator', 'episode')
