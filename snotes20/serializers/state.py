from rest_framework.serializers import ModelSerializer

from snotes20.models import DocumentStateError, OSFNote


class DocumentStateErrorSerializer(ModelSerializer):
    class Meta:
        model = DocumentStateError
        fields = ('line', 'message')


class OSFNoteSerializer(ModelSerializer):
    class Meta:
        model = OSFNote
        fields = ('title', 'url')
