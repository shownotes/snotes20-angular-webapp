from django.contrib import admin
import django.forms as forms
from django.forms.utils import ErrorList

import snotes20.models as models

@admin.register(models.Podcast)
class PodcastAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    pass

class DocumentAdminForm(forms.ModelForm):
    episode = forms.ModelChoiceField(queryset=models.Episode.objects.all(), required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):

        try:
            initial = {'episode': instance.episode}
        except models.Episode.DoesNotExist:
            pass

        super(DocumentAdminForm, self).__init__(data=data, files=files, auto_id=auto_id, prefix=prefix,
                                                initial=initial, error_class=error_class, label_suffix=label_suffix,
                                                empty_permitted=empty_permitted, instance=instance)

    class Meta:
        model = models.Document

@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['episode'] is not None:
            ep = form.cleaned_data['episode']
            obj.episode = ep
            form.cleaned_data['episode'].save()
        else:
            ep = obj.episode
            obj.episode.document = None

        ep.save()

        admin.ModelAdmin.save_model(self, request, obj, forms, change)

@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass

@admin.register(models.PublicationRequest)
class PublicationRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(models.NUser)
class NUserAdmin(admin.ModelAdmin):
    pass
