from django.db import models
from django.contrib.flatpages.models import FlatPage
from ckeditor.fields import RichTextField


class ExtendedFlatPage(FlatPage):
    order = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ['order']
