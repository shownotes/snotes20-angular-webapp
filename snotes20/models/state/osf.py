from django.db import models, transaction

from osf import OSFLine

from .DocumentState import DocumentState


class OSFDocumentState(DocumentState):

    def to_dict(self):
        return {
            "shownotes": self.get_shownotes_list(),
            "header": {}
        }

    def get_shownotes_list(self, notes=None, level=0):
        root = []

        if not notes:
            notes = self.shownotes

        for note in notes.all().order_by('order'):
            me = note.to_dict(level)
            me['shownotes'] = self.get_shownotes_list(notes=note.shownotes, level=level + 1)
            root.append(me)

        return root

    def __str__(self):
        return "OSFDocumentState, " + str(self.shownotes.count()) + " notes"


class OSFTag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    short = models.CharField(max_length=20, unique=True, db_index=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return "#" + self.name + " (#" + self.short + ")"

    def absorb_tag_as_short(self, tag):
        self.short = tag.name

        with transaction.atomic():
            self.save()
            OSFNote.tags.through.objects.filter(osftag_id=tag.pk).exclude(osftag_id=self.pk).update(osftag_id=self.pk)
            tag.remove()


class OSFNote(models.Model):
    state = models.ForeignKey(OSFDocumentState, related_name="shownotes", null=True, blank=True)
    parent = models.ForeignKey('self', related_name="shownotes", null=True, blank=True)
    order = models.IntegerField()
    timestamp = models.BigIntegerField(null=True)
    title = models.TextField()
    url = models.URLField(null=True)
    tags = models.ManyToManyField(OSFTag, related_name="notes")

    def to_dict(self, level):
        return {
            'timestamp': self.timestamp,
            'title': self.title,
            'url': self.url,
            'revision': 'revision' in self.tags.all(),
            'valid': True,
            'errorMessages': [],
            'tags': [tag.name for tag in self.tags.all()],
            'level': level,
        }

    class Meta:
        unique_together = ('order', 'state')
