from django.contrib.auth import get_user_model

from rest_framework import serializers

import snotes20.models as models


class NUserSocialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NUserSocialType


class NUserSocialSerializer(serializers.ModelSerializer):
    type = NUserSocialTypeSerializer()

    class Meta:
        model = models.NUserSocial
        fields = ('id', 'type', 'value')
        depth = 1


class NUserSerializer(serializers.ModelSerializer):
    socials = NUserSocialSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'color', 'date_joined', 'groups', 'socials')
