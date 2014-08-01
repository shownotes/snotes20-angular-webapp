from django.db import models

from uuidfield import UUIDField

from .DocumentState import DocumentState


class OSFDocumentState(DocumentState):
    pass


class OSFTag(models.Model):
    name = models.CharField(max_length=50)
    short = models.CharField(max_length=20)
    description = models.CharField(max_length=200)


class OSFNote(models.Model):
    state = models.ForeignKey(OSFDocumentState, related_name="notes")
    order = models.IntegerField()
    time = models.PositiveIntegerField(null=True)
    indentation = models.PositiveIntegerField()
    text = models.CharField(max_length=300)
    link = models.URLField(null=True)
    tags = models.ManyToManyField(OSFTag, related_name="notes")

    class Meta:
        unique_together = ('order', 'state')
