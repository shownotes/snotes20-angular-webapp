from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm, UserCreationForm
import django.forms as forms
import django.db.models as dmodels

import snotes20.models as models
import snotes20.reverseadmins as reverse

class PodcastSlugInline(admin.TabularInline):
    model = models.PodcastSlug
    extra = 0

class EpisodeInline(admin.TabularInline):
    model = models.Episode
    extra = 0
    fields = ('date', 'number', 'episode_url', 'type', 'document')

    formfield_overrides = {
        dmodels.CharField: {'widget': forms.TextInput(attrs={'size': '20'})},
        dmodels.URLField: {'widget': forms.TextInput(attrs={'size': '20'})},
    }

@admin.register(models.Podcast)
class PodcastAdmin(admin.ModelAdmin):
    inlines = [PodcastSlugInline, EpisodeInline]

    search_fields = ('slugs__slug', 'source_id', 'title', 'url')
    readonly_fields = ('slug',)
    fieldsets = (
        (None, {
            'fields': ('slug', 'title', 'description', 'url', 'type')
        }),
        ('Live', {
            'fields': ('stream', 'chat')
        }),
        ('Validity', {
            'fields': ('deleted', 'approved')
        }),
        ('Import', {
            'classes': ('collapse',),
            'fields': ('source', 'source_id', 'import_date')
        }),
        ('Creation', {
            'classes': ('collapse',),
            'fields': ('creator', 'create_date')
        }),
    )

class PublicationInline(admin.StackedInline):
    model = models.Publication
    extra = 0
    fields = ('creator', ('comment', 'preliminary'), 'state')
    readonly_fields = ('state',)

    def has_add_permission(self, request):
        return False

@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    inlines = (PublicationInline,)
    fieldsets = (
        (None, {
            'fields': ('podcast', 'number', 'type', 'episode_url')
        }),
        ('Live', {
            'fields': (('date', 'canceled'), 'stream', 'document')
        }),
        ('Import', {
            'classes': ('collapse',),
            'fields': ('source', 'source_id', 'import_date')
        }),
        ('Creation', {
            'classes': ('collapse',),
            'fields': ('creator', 'create_date')
        }),
    )

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


class NUserSocialInline(admin.TabularInline):
    model = models.NUserSocial
    extra = 0


class NUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.NUser


class NUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = models.NUser

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            models.NUser.objects.get(username=username)
        except models.NUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        user = super(NUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

UserAdmin.fieldsets = (
    (UserAdmin.fieldsets[0][0], {'fields': ('username', 'password', 'migrated')}),
    (UserAdmin.fieldsets[1][0], {'fields': ('email', 'color')}),
    (UserAdmin.fieldsets[2][0], {'fields': ('groups',)}),
    (UserAdmin.fieldsets[3][0], {'fields': (('date_login', 'date_joined'),)})
)
UserAdmin.list_display = ('username', 'email', 'is_staff')
UserAdmin.readonly_fields = ('migrated',)
UserAdmin.add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

@admin.register(models.NUser)
class NUserAdmin(UserAdmin):
    inlines = [NUserSocialInline,]
    form = NUserChangeForm
    add_form = NUserCreationForm

@admin.register(models.NUserSocialType)
class NUserSocialTypeAdmin(admin.ModelAdmin):
    pass
