import snotes20.models as models
import snotes20.editors as editors

from .osf import handle as osf
from .txt import handle as txt


def get_state(doc):
    editor = editors.EditorFactory.get_editor(doc.editor)
    text = editor.get_document_text(doc)

    raw_state = txt(text)

    if doc.type == models.CONTENTTYPE_TXT:
        state = raw_state
    elif doc.type == models.CONTENTTYPE_OSF:
        state = osf(text)
    else:
        raise Exception()

    raw_state.save()
    state.save()

    return raw_state, state
