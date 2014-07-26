from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from snotes20.models import Document, DocumentMeta
from snotes20.serializers import EpisodeSerializer


class DocumentMetaSerializer(ModelSerializer):
    def __init__(self, *kargs, **kwargs):
        super(DocumentMetaSerializer, self).__init__(*kargs, **kwargs)

    def field_to_native(self, obj, field_name):
        data = super(DocumentMetaSerializer, self).field_to_native(obj, field_name)

        try:
            meta = obj.meta
        except DocumentMeta.DoesNotExist:
            meta = None

        if meta is not None:
            data['shownoters'] = [shownoter.username for shownoter in meta.shownoters.all()]


        return data

    class Meta:
        model = DocumentMeta
        fields = ('podcasters',)
        depth = 1


class DocumentSerializer(ModelSerializer):
    episode = EpisodeSerializer()
    meta = DocumentMetaSerializer()

    class Meta:
        model = Document
        fields = ('name', 'editor', 'create_date', 'episode', 'meta')
