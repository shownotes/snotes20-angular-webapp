from django.db import models
from django.contrib.auth.models import User

from uuidfield import UUIDField

from snotes20.models import Episode, DocumentState


class Publication(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    episode = models.ForeignKey(Episode)
    creator = models.ForeignKey(User)
    state = models.ForeignKey(DocumentState, unique=True)
    preliminary = models.BooleanField(default=False)
    comment = models.CharField(max_length=250)


class PublicationRequest(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    publication = models.OneToOneField(Publication, null=True)
    episode = models.ForeignKey(Episode)
    requester = models.ForeignKey(User)
    state = models.ForeignKey(DocumentState, unique=True)
    preliminary = models.BooleanField(default=False)
    comment = models.CharField(max_length=250)
