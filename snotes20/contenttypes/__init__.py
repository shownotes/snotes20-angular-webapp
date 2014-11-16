import snotes20.models as models
import snotes20.editors as editors

from .osf import handle as osf
from .txt import handle as txt

def prep_state(doc):
    editor = editors.EditorFactory.get_editor(doc.editor)
    text = editor.get_document_text(doc)

    return {
        'text': text,
        'type': doc.type
    }


def get_state(prepped):
    # this in run inside a transaction, so keep the execution time as short as possible
    # all HTTP requests are made in prep_state, instead of here.

    text = prepped['text']
    type = prepped['type']

    raw_state = txt(text)

    if type == models.CONTENTTYPE_TXT:
        state = raw_state
    elif type == models.CONTENTTYPE_OSF:
        state = osf(text)
    else:
        raise Exception()

    raw_state.save()
    state.save()

    return raw_state, state
