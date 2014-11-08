import snotes20.models as models


def handle(text):
    raw_state = models.TextDocumentState()
    raw_state.text = text

    return raw_state