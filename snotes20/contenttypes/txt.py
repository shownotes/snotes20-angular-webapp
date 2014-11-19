import snotes20.models as models


def prep(text):
    return text


def handle(prep):
    raw_state = models.TextDocumentState()
    raw_state.text = prep

    return raw_state