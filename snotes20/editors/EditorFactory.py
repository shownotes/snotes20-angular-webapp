from django.conf import settings

from .etherpad import EtherpadEditor


class UnknownEditorException(Exception):
    pass


class EditorFactory:
    _editorCache = {}

    @classmethod
    def get_editor(cls, name):
        cache = EditorFactory._editorCache

        if name not in cache:
            config = settings.EDITORS.get(name, None)

            if name == 'EP':
                instance = EtherpadEditor(config)
            else:
                raise UnknownEditorException()

            cache[name] = instance

        return cache[name]