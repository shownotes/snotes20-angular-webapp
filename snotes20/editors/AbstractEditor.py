from abc import ABCMeta, abstractmethod

class AbstractEditor:
    __metaclass__ = ABCMeta

    def __init__(self, config):
        self.secret = config['secret']
        self.userurl = config['userurl']
        self.apiurl = config['apiturl']

    @abstractmethod
    def get_session(self, user):
        pass
  
    @abstractmethod
    def delete_session(self, sid):
        pass

    @abstractmethod
    def delete_sessions(self, user):
        pass

    @abstractmethod
    def create_document(self, docname):
        pass

    @abstractmethod
    def delete_document(self, docname):
        pass

    @abstractmethod
    def set_document_text(self, docname, text):
        pass
