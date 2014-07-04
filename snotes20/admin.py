from django.contrib import admin

import snotes20.models as models

@admin.register(models.Podcast)
class PodcastAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass

@admin.register(models.PublicationRequest)
class PublicationRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(models.NUser)
class NUserAdmin(admin.ModelAdmin):
    pass
