import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q

import snotes20.models as models
import snotes20.editors as editors
import osf
import modgrammar


logger = logging.getLogger(__name__)


def find_or_create_osf_tag(short):
    try:
        return models.OSFTag.objects.get(Q(short=short) | Q(name=short))
    except models.OSFTag.DoesNotExist:
        tag = models.OSFTag(name=short)
        tag.save()
        return tag



class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        docs = models.Document.objects.all()

        for doc in docs:
            logger.debug("Document:" + doc.name)

            with transaction.atomic():
                if doc.state:
                    doc.state.delete()
                if doc.raw_state:
                    doc.raw_state.delete()

                editor = editors.EditorFactory.get_editor(doc.editor)
                text = editor.get_document_text(doc)

                raw_state = models.TextDocumentState()
                raw_state.text = text
                raw_state.save()

                doc.raw_state = raw_state
                doc.save()

                if doc.type == models.CONTENTTYPE_TXT:
                    doc.state = raw_state
                    doc.save()
                elif doc.type == models.CONTENTTYPE_OSF:
                    state = models.OSFDocumentState()
                    
                    header, p_lines = osf.parse_lines(text.split('\n'))
                    o_lines = osf.objectify_lines(p_lines)

                    state.save()
                    doc.state = state
                    doc.save()

                    for index, line in enumerate(o_lines):
                        if isinstance(line, modgrammar.ParseError):
                            error = models.DocumentStateError(
                                state=state,
                                line=line.line,
                                message=line.message
                            )

                            error.save()
                        else:
                            note = models.OSFNote(
                                state=state,
                                time=line.time,
                                indentation=line.indentation,
                                text=line.text,
                                link=line.link,
                                order=index
                            )

                            note.save()
                            note.tags.add(*[find_or_create_osf_tag(tag) for tag in o_lines[index].tags])
                else:
                    raise Exception()

