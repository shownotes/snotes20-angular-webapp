from datetime import datetime

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete

from uuidfield import UUIDField

from .state import DocumentState

EDITOR_ETHERPAD  = 'EP'

EDITOR_CHOICES = (
    (EDITOR_ETHERPAD, 'Etherpad'),
)


class DocumentMeta(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    state = models.ForeignKey(DocumentState, null=True, blank=True)
    shownoters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return "Meta for " + self.document.__str__()


class RawPodcaster(models.Model):
    meta = models.ForeignKey(DocumentMeta, related_name="podcasters")
    name = models.CharField(max_length=30)


class Document(models.Model):
    name = models.CharField(primary_key=True, max_length=40)
    editor = models.CharField(max_length=3, choices=EDITOR_CHOICES)
    create_date = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    meta = models.OneToOneField(DocumentMeta, related_name='document', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        try:
            epi = str(self.episode)
        except:
            epi = "no episode"

        return "Document {} ({})".format(self.name, epi)

@receiver(post_delete, sender=Document)
def doc_post_delete_meta(sender, instance, *args, **kwargs):
    if instance.meta:
        instance.meta.delete()

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
