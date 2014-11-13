from rest_framework.serializers import ModelSerializer, Field

from snotes20.models import Cover


class CoverSerializer(ModelSerializer):

    class Meta:
        model = Cover
        fields = ('id', 'file', 'create_date')
