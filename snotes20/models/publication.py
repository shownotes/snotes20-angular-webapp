from django.db import models
from django.conf import settings

from uuidfield import UUIDField

from .podcast import Episode
from .state import DocumentState


class Podcaster(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    uri = models.URLField(unique=True, db_index=True)
    name = models.CharField(max_length=30)


class Publication(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    create_date = models.DateTimeField()
    state = models.ForeignKey(DocumentState)
    episode = models.ForeignKey(Episode)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    shownoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contributed_publications')
    podcasters = models.ManyToManyField(Podcaster, related_name='contributed_publications')
    preliminary = models.BooleanField(default=False)
    comment = models.CharField(max_length=250)


class PublicationRequest(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    state = models.ForeignKey(DocumentState)
    episode = models.ForeignKey(Episode)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    shownoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contributed_publicationrequests')
    podcasters = models.ManyToManyField(Podcaster, related_name='contributed_publicationrequests')
    preliminary = models.BooleanField(default=False)
    comment = models.CharField(max_length=250)
    publication = models.OneToOneField(Publication, null=True)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requested_publicationrequests')
