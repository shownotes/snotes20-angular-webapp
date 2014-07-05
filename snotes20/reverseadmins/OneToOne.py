import django.forms as forms
import django.forms.widgets as widgets
from django.contrib import admin


class ReverseOneToOneAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs and kwargs['initial'] is not None:
            initial = kwargs['initial']
        else:
            initial = {}

        for rel in self.rels:
            initial[rel] = getattr(kwargs['instance'], rel, None)

        kwargs['initial'] = initial
        super(ReverseOneToOneAdminForm, self).__init__(*args, **kwargs)


class ReverseOneToOneAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        for rel in self.rels:
            name = rel[0]
            rname = rel[1]

            if form.cleaned_data[name] is not None:
                other = form.cleaned_data[name]
                setattr(obj, name, other)
            else:
                other = obj.episode
                setattr(other, rname, None)

            other.save()

        admin.ModelAdmin.save_model(self, request, obj, forms, change)