from django.db import transaction
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
        fields = ('type', 'value')
        depth = 1


class NUserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)

    def __init__(self, *kargs, **kwargs):
        super(NUserSerializer, self).__init__(*kargs, **kwargs)

        self._socials = []

        if len(kargs) > 0:
            instance = kargs[0]
            self.data['socials'] = {}

            for social in instance.socials.all():
                self.data['socials'][social.type.name] = social.value

    def restore_fields(self, data, files):
        reverted_data = super(NUserSerializer, self).restore_fields(data, files)
        if 'socials' in data:
            reverted_data['socials'] = data['socials']
        return reverted_data

    def restore_object(self, attrs, instance=None):
        socials = None
        if 'socials' in attrs:
            socials = attrs.pop('socials') # rescue before the super restore_object pops it..

        instance = super(NUserSerializer, self).restore_object(attrs, instance)

        if socials is not None:
            self._socials = []
            for type, value in socials.items():
                found_social = None

                for social in instance.socials.all():
                    if social.type.name == type:
                        found_social = social
                        break

                if found_social is not None:
                    found_social.value = value
                    self._socials.append(found_social)
                else:
                    social = models.NUserSocial(user=instance, type=models.NUserSocialType.objects.get(name=type), value=value)
                    self._socials.append(social)
        else:
            self._socials = None

        return instance

    def save(self, **kwargs):
        obj = super(NUserSerializer, self).save(**kwargs)

        if self._socials is not None:
            with transaction.atomic():
                obj.socials.all().delete()
                for social in self._socials:
                    social.user = obj
                    social.save()

        return obj

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'color', 'date_joined', 'date_login', 'is_staff', 'groups', 'bio')


class NUserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
