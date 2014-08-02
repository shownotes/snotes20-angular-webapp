from datetime import datetime

from django.db import models

from uuidfield import UUIDField


class DocumentState(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    date = models.DateTimeField(default=datetime.now)


class DocumentStateError(models.Model):
    state = models.ForeignKey(DocumentState, related_name="errors")
    line = models.PositiveIntegerField()
    message = models.CharField(max_length=400)
