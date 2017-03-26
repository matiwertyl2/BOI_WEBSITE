from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage

from .models import ExtendedFlatPage
from django import forms
from ckeditor.widgets import CKEditorWidget


class ExtendedFlatPageForm(FlatpageForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = ExtendedFlatPage
        fields = ('url', 'title', 'content', 'sites', 'order')


class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'order')}),
    )


admin.site.unregister(FlatPage)
admin.site.register(ExtendedFlatPage, ExtendedFlatPageAdmin)
