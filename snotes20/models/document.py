from datetime import datetime

from django.db import models
from django.conf import settings

from uuidfield import UUIDField

from .state.DocumentState import DocumentMetaData


EDITOR_ETHERPAD  = 'EP'

EDITOR_CHOICES = (
    (EDITOR_ETHERPAD, 'Etherpad'),
)


class Document(models.Model):
    name = models.CharField(primary_key=True, max_length=40)
    editor = models.CharField(max_length=3, choices=EDITOR_CHOICES)
    create_date = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    meta = models.ForeignKey(DocumentMetaData)

    def save(self, *kargs, **kwargs):
        if self.meta_id is None:
            meta = DocumentMetaData()
            meta.save()
            self.meta = meta
        super(Document, self).save(*kargs, **kwargs)

    def __str__(self):
        try:
            epi = str(self.episode)
        except:
            epi = "no episode"

        return "Document {} ({})".format(self.name, epi)


CHAT_MSG_ISSUER_USER = 'USR'

CHAT_MSG_ISSUER_CHOICES = (
    (CHAT_MSG_ISSUER_USER, 'User'),
)


class ChatMessageIssuer(models.Model):
    type = models.CharField(max_length=3, choices=CHAT_MSG_ISSUER_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class ChatMessage(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    document = models.ForeignKey(Document, related_name='messages')
    issuer = models.OneToOneField(ChatMessageIssuer)
    message = models.CharField(max_length=200)
