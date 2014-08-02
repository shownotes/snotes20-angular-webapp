from rest_framework.serializers import ModelSerializer

from snotes20.models import DocumentStateError


class DocumentStateErrorSerializer(ModelSerializer):
    class Meta:
        model = DocumentStateError
        fields = ('line', 'message')
