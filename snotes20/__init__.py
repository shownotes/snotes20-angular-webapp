from django.db.models.signals import post_save

import snotes20.models as models
import snotes20.editors as editors


def editor_create_doc(sender, instance, created, **kwargs):
    if created:
        editor = editors.EditorFactory.get_editor(instance.editor)
        editor.create_document(instance)


def editor_delete_doc(sender, instance, **kwargs):
    editor = editors.EditorFactory.get_editor(instance.editor)
    editor.delete_document(instance)


post_save.connect(editor_create_doc, sender=models.Document, dispatch_uid='editor_create_doc')
post_save.connect(editor_delete_doc, sender=models.Document, dispatch_uid='editor_delete_doc')
