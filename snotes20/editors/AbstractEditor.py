from abc import ABCMeta, abstractmethod

class AbstractEditor:
    __metaclass__ = ABCMeta

    def __init__(self, config):
        self.secret = config['secret']
        self.userurl = config['userurl']
        self.apiurl = config['apiurl']

    @abstractmethod
    def get_session(self, document, user):
        pass
  
    @abstractmethod
    def delete_session(self, sid):
        pass

    @abstractmethod
    def delete_sessions(self, user):
        pass

    @abstractmethod
    def create_document(self, document):
        pass

    @abstractmethod
    def delete_document(self, document):
        pass

    @abstractmethod
    def set_document_text(self, document, text):
        pass
