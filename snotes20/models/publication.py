from django.db import models
from django.conf import settings

from uuidfield import UUIDField

from .podcast import Episode
from .state import DocumentState, TextDocumentState


class Podcaster(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    uri = models.URLField(unique=True, db_index=True)
    name = models.CharField(max_length=30)


class PubBase(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    create_date = models.DateTimeField()
    comment = models.CharField(max_length=250,  blank=True, null=True)

    class Meta:
        abstract = True


class Publication(PubBase):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_publications")
    episode = models.ForeignKey(Episode, related_name="publications")
    shownoters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='contributed_publications')
    podcasters = models.ManyToManyField(Podcaster, blank=True, related_name='contributed_publications')
    preliminary = models.BooleanField(default=False)
    state = models.ForeignKey(DocumentState, related_name="+")
    raw_state = models.ForeignKey(TextDocumentState, related_name="+")


class PublicationRequest(PubBase):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requested_publicationrequests')
    episode = models.ForeignKey(Episode, related_name="publicationrequests")
