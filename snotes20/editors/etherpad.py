from .AbstractEditor import AbstractEditor

class EtherpadEditor(AbstractEditor):

    def __init__(self, config):
        AbstractEditor.__init__(self, config)

    def get_session(self, user):
        pass

    def delete_session(self, sid):
        pass

    def delete_sessions(self, user):
        pass

    def create_document(self, docname):
        pass

    def delete_document(self, docname):
        pass

    def set_document_text(self, docname, text):
        pass
