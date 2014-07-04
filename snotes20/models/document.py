from datetime import datetime

from django.db import models
from django.conf import settings

from uuidfield import UUIDField


EDITOR_ETHERPAD  = 'EP'

EDITOR_CHOICES = (
    (EDITOR_ETHERPAD, 'Etherpad'),
)


class Document(models.Model):
    name = models.CharField(primary_key=True, max_length=25)
    editor = models.CharField(max_length=3, choices=EDITOR_CHOICES)
    create_date = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        try:
            epi = str(self.episode)
        except:
            epi = "no episode"

        return "Document {} ({})".format(self.name, epi)


class ChatMessageIssuer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class ChatMessage(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    document = models.ForeignKey(Document)
    issuer = models.ForeignKey(ChatMessageIssuer)
    message = models.CharField(max_length=200)


class Podcaster(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    uri = models.URLField(unique=True, db_index=True)
    name = models.CharField(max_length=30)


class DocumentMetaData(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    document = models.ForeignKey(Document)
    podcasters = models.ManyToManyField(Podcaster)


