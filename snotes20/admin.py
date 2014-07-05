from django.contrib import admin
import django.forms as forms

import snotes20.models as models
import snotes20.reverseadmins as reverse

@admin.register(models.Podcast)
class PodcastAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    pass

class DocumentAdminForm(reverse.ReverseOneToOneAdminForm):
    rels = ('episode',)
    episode = forms.ModelChoiceField(queryset=models.Episode.objects.all(), required=False)

    class Meta:
        model = models.Document

@admin.register(models.Document)
class DocumentAdmin(reverse.ReverseOneToOneAdmin):
    form = DocumentAdminForm
    rels = (('episode', 'document'),)

@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass

@admin.register(models.PublicationRequest)
class PublicationRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(models.NUser)
class NUserAdmin(admin.ModelAdmin):
    pass
