from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from uuidfield import UUIDField


EDITOR_ETHERPAD  = 'EP'

EDITOR_CHOICES = (
    (EDITOR_ETHERPAD, 'Etherpad'),
)


class Document(models.Model):
    name = models.CharField(primary_key=True, max_length=25)
    editor = models.CharField(max_length=3, choices=EDITOR_CHOICES)
    create_date = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(User, null=True)


class ChatMessageIssuer(models.Model):
    user = models.ForeignKey(User)


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


