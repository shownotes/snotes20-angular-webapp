from datetime import datetime

from django.db import models

from uuidfield import UUIDField


class DocumentState(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    date = models.DateTimeField(default=datetime.now)
