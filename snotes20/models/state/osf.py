from django.db import models

from .DocumentState import DocumentState


class OSFDocumentState(DocumentState):
    id = models.AutoField(primary_key=True)
    notes = models.OneToOneField(OSFNote)


class OSFNote(models.Model):
    state = models.ForeignKey(OSFDocumentState, primary_key=True)
    order = models.IntegerField(primary_key=True)
    time = models.IntegerField(null=True)
    text = models.CharField(300)
    link = models.URLField(null=True)
    tags = models.ManyToManyField(OSFTag)



class OSFTag(models.Model):
    name = models.CharField(max_length=50)
    short = models.CharField(max_length=20)
    description = models.CharField(max_length=200)