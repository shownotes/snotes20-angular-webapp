from django.db.models import Q

import snotes20.models as models

import osf
import modgrammar


def find_or_create_osf_tag(short):
    try:
        return models.OSFTag.objects.get(Q(short=short) | Q(name=short))
    except models.OSFTag.DoesNotExist:
        tag = models.OSFTag(name=short)
        tag.save()
        return tag


def add_osf_note(state, line, parent=None):
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
            parent=parent,
            timestamp=line.time,
            title=line.text,
            url=line.link,
            order=line._line
        )

        note.save()
        note.tags.add(*[find_or_create_osf_tag(tag) for tag in line.tags])

        for nnote in line.notes:
            add_osf_note(state, nnote, note)


def handle(text):
    state = models.OSFDocumentState()

    header, p_lines = osf.parse_lines(text.split('\n'))
    o_lines = osf.objectify_lines(p_lines)

    state.save()

    for line in o_lines:
        add_osf_note(state, line)

    return state
