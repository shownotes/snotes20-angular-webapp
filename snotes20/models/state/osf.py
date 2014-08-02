from django.db import models

from osf import OSFLine

from .DocumentState import DocumentState


class OSFDocumentState(DocumentState):

    def to_osf_str(self):
        return "\n".join([note.to_osf_str() for note in self.notes])

    def __str__(self):
        return "OSFDocumentState, " + self.notes.count() + " notes"


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

    def __str__(self):
        return str(self.to_OSFLine())

    def to_OSFLine(self):
        line = OSFLine()
        line.time = self.time
        line.indentation = self.indentation
        line.text = self.text
        line.link = self.link
        line.tags = [tag.short for tag in self.tags]
        return line

    class Meta:
        unique_together = ('order', 'state')
