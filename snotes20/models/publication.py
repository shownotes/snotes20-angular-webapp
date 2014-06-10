from django.db import models
from django.contrib.auth.models import User

from snotes20.models import Episode, DocumentState


class Publication(models.Model):
    id = models.AutoField(primary_key=True)
    episode = models.ForeignKey(Episode)
    creator = models.ForeignKey(User)
    state = models.ForeignKey(DocumentState, unique=True)
    preliminary = models.BooleanField(default=False)
    comment = models.CharField(max_length=250)


class PublicationRequest(models.Model):
    id = models.AutoField(primary_key=True)
    publication = models.OneToOneField(Publication, null=True)
    episode = models.ForeignKey(Episode)
    requester = models.ForeignKey(User)
    state = models.ForeignKey(DocumentState, unique=True)
    preliminary = models.BooleanField(default=False)
    comment = models.CharField(max_length=250)
