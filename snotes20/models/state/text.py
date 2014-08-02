from django.db import models

from .DocumentState import DocumentState


class TextDocumentState(DocumentState):
    text = models.TextField()

    def to_osf_str(self):
        return self.text

    def __str__(self):
        return "OSFDocumentState, " + str(len(self.text)) + " chars"
