import snotes20.models as models
import snotes20.editors as editors

from .osf import handle as osf_handle
from .osf import prep as osf_prep
from .txt import handle as txt_handle
from .txt import prep as txt_prep


def prep_state(doc):
    editor = editors.EditorFactory.get_editor(doc.editor)
    text = editor.get_document_text(doc)

    if doc.type == models.CONTENTTYPE_TXT:
        handle_prep = txt_prep(text)
    elif doc.type == models.CONTENTTYPE_OSF:
        handle_prep = osf_prep(text)
    else:
        raise Exception()

    return {
        'text': text,
        'type': doc.type,
        'handle_prep': handle_prep
    }


def get_state(prepped):
    # this in run inside a transaction, so keep the execution time as short as possible
    # all HTTP requests are made in prep_state, instead of here.

    text = prepped['text']
    type = prepped['type']

    raw_state = txt_handle(text)

    if type == models.CONTENTTYPE_TXT:
        state = raw_state
    elif type == models.CONTENTTYPE_OSF:
        state = osf_handle(prepped['handle_prep'])
    else:
        raise Exception()

    raw_state.save()
    state.save()

    return raw_state, state
