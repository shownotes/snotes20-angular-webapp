from django.db import models

from osf import OSFLine

from .DocumentState import DocumentState


class OSFDocumentState(DocumentState):

    def to_list(self, notes=None, depth=0):
        root = []

        if not notes:
            notes = self.notes

        for note in notes.all():
            me = note.to_dict(depth)
            me['notes'] = self.to_list(notes=note.notes, depth=depth + 1)
            root.append(me)

        return root

    def __str__(self):
        return "OSFDocumentState, " + str(self.notes.count()) + " notes"


class OSFTag(models.Model):
    name = models.CharField(max_length=50)
    short = models.CharField(max_length=20)
    description = models.CharField(max_length=200)


class OSFNote(models.Model):
    state = models.ForeignKey(OSFDocumentState, related_name="notes")
    parent = models.ForeignKey('self', related_name="notes", null=True, blank=True)
    order = models.IntegerField()
    time = models.PositiveIntegerField(null=True)
    text = models.CharField(max_length=300)
    link = models.URLField(null=True)
    tags = models.ManyToManyField(OSFTag, related_name="notes")

    def to_dict(self, depth):
        me = {
            'time': self.time,
            'text': self.text,
            'link': self.link,
            'tags': {tag.name: True for tag in self.tags.all()},
            'depth': depth,
        }

        return me

    class Meta:
        unique_together = ('order', 'state')
