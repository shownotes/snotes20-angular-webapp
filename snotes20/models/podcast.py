from datetime import datetime

from django.db import models
from django.conf import settings

from uuidfield import UUIDField

from .document import Document


SOURCE_INTERNAL = 'INT'
SOURCE_HOERSUPPE = 'HOE'

SOURCE_CHOICES = (
    (SOURCE_INTERNAL, 'Internal'),
    (SOURCE_HOERSUPPE, 'Hoersuppe'),
)


class Importable(models.Model):
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, db_index=True)
    source_id = models.IntegerField(null=True, blank=True, verbose_name="ID at source", db_index=True)
    import_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


TYPE_PODCAST = 'POD'
TYPE_EVENT = 'EVT'
TYPE_RADIO = 'RAD'

TYPE_CHOICES = (
    (TYPE_PODCAST, 'Podcast'),
    (TYPE_EVENT, 'Event'),
    (TYPE_RADIO, 'Radio'),
)


class Podcast(Importable):
    id = UUIDField(primary_key=True, auto=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    url = models.URLField()
    stream = models.CharField(max_length=100, null=True, blank=True)
    chat = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    deleted = models.BooleanField(default=False)
    approved= models.BooleanField(default=False)
    create_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        try:
            return "Podcast {} ({})".format(self.title, self.slug)
        except models.ObjectDoesNotExist:
            return "Podcast no slug!"

    @property
    def slug(self):
        return str(self.slugs.latest())


class PodcastSlug(models.Model):
    podcast = models.ForeignKey(Podcast, related_name="slugs")
    slug = models.SlugField(unique=True, db_index=True)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.slug

    class Meta:
        get_latest_by = 'date_added'

class Episode(Importable):
    id = UUIDField(primary_key=True, auto=True)
    podcast = models.ForeignKey(Podcast)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    episode_url = models.URLField(verbose_name="Episode URL", null=True, blank=True)
    date = models.DateTimeField()
    canceled = models.BooleanField(default=False)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    create_date = models.DateTimeField(default=datetime.now)
    stream = models.CharField(max_length=100, null=True, blank=True)
    document = models.OneToOneField(Document, null=True, blank=True, unique=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Episode {}-{} ({})".format(self.podcast.slug, self.number or 'NoNumberYet', self.date)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = None
        super(Episode, self).save(*args, **kwargs)
