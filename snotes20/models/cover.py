import uuid
import urllib.request
from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.image import Image

from uuidfield import UUIDField

valid_exts = ('jpg', 'jpeg', 'png',)


# http://stackoverflow.com/a/15141228/2486196
def f(instance, filename):
    ext = filename.split('.')[-1]

    if ext not in valid_exts:
        raise Exception('invalid extension')

    return 'covers/{}.{}'.format(str(uuid.uuid4()), ext)


class Cover(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    file = models.ImageField(upload_to=f)
    original_url = models.URLField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    create_date = models.DateTimeField()

    @staticmethod
    def from_url(creator, url):
        try:
            return Cover.objects.get(original_url=url)
        except Cover.DoesNotExist:
            pass

        img_temp = None

        try:
            cover = Cover(creator=creator, create_date=datetime.now(), original_url=url)

            response = urllib.request.urlopen(url)

            if 'content-length' not in response.headers or int(response.headers['content-length']) > 100000:
                return None

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.read())
            img_temp.flush()

            Image.open(img_temp.name).verify()

            cover.file.save(f(None, url), File(img_temp), save=True)

            return cover
        except:
            return None
        finally:
            if img_temp:
                img_temp.close()

