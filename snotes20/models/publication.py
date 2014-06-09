from django.db import models
from django.contrib.auth.models import User

from .podcast import Episode
from .state import DocumentState


class Publication(models.Model):
    id = models.AutoField(primary_key=True)
    episode = models.ForeignKey(Episode)
    creator = models.ForeignKey(User)
    state = models.ForeignKey(DocumentState, unique=True)
    preliminary = models.BooleanField()
    comment = models.CharField()


class PublicationRequest(models.Model):
    id = models.AutoField(primary_key=True)
    publication = models.ForeignKey(Publication, null=True)
    episode = models.ForeignKey(Episode)
    requester = models.ForeignKey(User)
    state = models.ForeignKey(DocumentState, unique=True)
    preliminary = models.BooleanField()
    comment = models.CharField()
