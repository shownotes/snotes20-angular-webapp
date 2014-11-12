import uuid

from django.db import models
from django.conf import settings

from uuidfield import UUIDField


# http://stackoverflow.com/a/15141228/2486196
def f(instance, filename):
    ext = filename.split('.')[-1]
    return 'covers/{}.{}'.format(str(uuid.uuid4()), ext)

class Cover(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    file = models.ImageField(upload_to=f)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    create_date = models.DateTimeField()
