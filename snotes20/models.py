from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    pass


SOURCE_INTERNAL = 'INT'
SOURCE_HOERSUPPE = 'HOE'

SOURCE_CHOICES = (
    (SOURCE_INTERNAL, 'Internal'),
    (SOURCE_HOERSUPPE, 'Hoersuppe'),
)


class Source(models.Model):
    name = models.CharField(max_length=100, primary_key=True, choices=SOURCE_CHOICES)
    description = models.CharField(max_length=50)


class Importable(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.ForeignKey(Source)
    source_id = models.IntegerField(null=True, db_index=True)


TYPE_PODCAST = 'POD'
TYPE_EVENT = 'EVT'
TYPE_RADIO = 'RAD'

TYPE_CHOICES = (
    (TYPE_PODCAST, 'Podcast'),
    (TYPE_EVENT, 'Event'),
    (TYPE_RADIO, 'Radio'),
)


class Podcast(Importable):
    slug = models.SlugField(unique=True, db_index=True)
    creator = models.ForeignKey(User, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    url = models.URLField()
    stream = models.CharField(max_length=100, null=True)
    chat = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    deleted = models.BooleanField(default=False)
    approved= models.BooleanField(default=False)
    createDate = models.DateTimeField()
    document = models.OneToOneField(Document, null=True)

    def __str__(self):
        return "Podcast " + self.slug


class Episode(Importable):
    podcast = models.ForeignKey(Podcast)
    creator = models.ForeignKey(User, null=True)
    number = models.CharField(max_length=10, null=True)
    episodeurl = models.URLField(null=True)
    date = models.DateTimeField()
    canceled= models.BooleanField(default=False)
    type=models.CharField(max_length=100, choices=TYPE_CHOICES)
    createDate = models.DateTimeField(),
    stream = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "Episode {} (nr: {}, pod: {})".format(self.id, self.number, self.podcast_id)
