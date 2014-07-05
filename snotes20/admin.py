from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm, UserCreationForm
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


class NUserSocialInline(admin.StackedInline):
    model = models.NUserSocial
    extra = 0



class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.NUser


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.NUser

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            models.NUser.objects.get(username=username)
        except models.NUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])



UserAdmin.fieldsets = (
    UserAdmin.fieldsets[0],
    (UserAdmin.fieldsets[1][0], {'fields': ('email', 'color')}),
    (UserAdmin.fieldsets[2][0], {'fields': ('groups',)}),
    UserAdmin.fieldsets[3],
)
UserAdmin.list_display = ('username', 'email', 'is_staff')

@admin.register(models.NUser)
class NUserAdmin(UserAdmin):
    inlines = [NUserSocialInline,]
    form = MyUserChangeForm
    add_form = MyUserCreationForm

@admin.register(models.NUserSocial)
class NUserSocialAdmin(admin.ModelAdmin):
    pass

@admin.register(models.NUserSocialType)
class NUserSocialTypeAdmin(admin.ModelAdmin):
    pass
