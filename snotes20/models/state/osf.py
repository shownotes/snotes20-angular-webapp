from django.db import models

from uuidfield import UUIDField

from .DocumentState import DocumentState


class OSFDocumentState(DocumentState):
    id = UUIDField(primary_key=True, auto=True)
    notes = models.OneToOneField(OSFNote)


class OSFNote(models.Model):
    state = models.ForeignKey(OSFDocumentState)
    order = models.IntegerField()
    time = models.IntegerField(null=True)
    text = models.CharField(300)
    link = models.URLField(null=True)
    tags = models.ManyToManyField(OSFTag)

    class Meta:
        unique_together = ('order', 'state')



class OSFTag(models.Model):
    name = models.CharField(max_length=50)
    short = models.CharField(max_length=20)
    description = models.CharField(max_length=200)