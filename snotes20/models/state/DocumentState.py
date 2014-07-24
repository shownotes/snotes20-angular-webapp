from django.db import models
from django.conf import settings

from uuidfield import UUIDField


class Podcaster(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    uri = models.URLField(unique=True, db_index=True)
    name = models.CharField(max_length=30)


class DocumentMetaData(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    podcasters = models.ManyToManyField(Podcaster, blank=True)
    shownoters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)


class DocumentState(models.Model):
    date = models.DateTimeField()
    metadata = models.ForeignKey(DocumentMetaData)
