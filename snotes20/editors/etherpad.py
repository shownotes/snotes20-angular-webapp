from datetime import datetime, timedelta

from etherpad_lite import EtherpadLiteClient, EtherpadException

from .AbstractEditor import AbstractEditor

class EtherpadEditor(AbstractEditor):

    def __init__(self, config):
        AbstractEditor.__init__(self, config)

        self.client = EtherpadLiteClient(
            base_params={'apikey':self.secret},
            base_url=self.apiurl,
            api_version="1.2.12"
        )

    def _get_authorid_for_user(self, user):
        name = user.username
        color = user.color
        if color is not None and len(color) > 0:
            color = '#' + color
        return self.client.createAuthorIfNotExistsFor(authorMapper=name, name=name, color=color)["authorID"]

    def _get_groupid_for_document(self, document):
        if isinstance(document, str):
            docname = document
        else:
            docname = document.name
        return self.client.createGroupIfNotExistsFor(groupMapper=docname)["groupID"]

    def _get_padid_for_document(self, document):
        group = self._get_groupid_for_document(document)
        return group + "$" + document.name

    def get_urlname_for_document(self, document):
        return self._get_padid_for_document(document)

    def generate_session(self, document, user):
        tomorrow = datetime.today() + timedelta(days=1)
        author = self._get_authorid_for_user(user)
        group = self._get_groupid_for_document(document)
        session = self.client.createSession(groupID=group, authorID=author, validUntil=tomorrow.timestamp())["sessionID"]
        return session

    def delete_session(self, sid):
        self.client.deleteSession(sessionID=sid)

    def delete_sessions(self, user):
        author = self._get_authorid_for_user(user)
        sessions = self.client.listSessionsOfAuthor(authorID=author)
        for sid in sessions:
            self.delete_session(sid)

    def create_document(self, document):
        group = self._get_groupid_for_document(document)
        try:
            self.client.createGroupPad(groupID=group, padName=document.name)
        except EtherpadException as e:
            if str(e) == 'padName does already exist':
                self.delete_document(document)
                self.client.createGroupPad(groupID=group, padName=document.name)
            else:
                raise

    def delete_document(self, document):
        pad_id = self._get_padid_for_document(document)
        self.client.deletePad(padID=pad_id)

    def set_document_text(self, document, text):
        pad_id = self._get_padid_for_document(document)
        self.client.setText(padID=pad_id, text=text)

    def get_document_text(self, document):
        pad_id = self._get_padid_for_document(document)
        return self.client.getText(padID=pad_id)["text"]
