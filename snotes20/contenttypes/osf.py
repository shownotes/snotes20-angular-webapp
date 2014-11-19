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
            timestamp=line.time,
            title=line.text,
            url=line.link,
            order=line._line
        )

        if parent is None:
            note.state = state
        else:
            note.parent = parent

        note.save()
        note.tags.add(*[find_or_create_osf_tag(tag) for tag in line.tags])

        for nnote in line.notes:
            add_osf_note(state, nnote, note)


def prep(text):
    header, p_lines = osf.parse_lines(text.split('\n'))
    o_lines = osf.objectify_lines(p_lines)

    return {
        'header': header,
        'p_lines': p_lines,
        'o_lines': o_lines
    }


def handle(prepped):
    state = models.OSFDocumentState()
    state.save()

    for line in prepped['o_lines']:
        add_osf_note(state, line)

    return state
