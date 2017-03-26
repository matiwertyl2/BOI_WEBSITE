from .models import ExtendedFlatPage


def ordered_pages(request):
    d = {}
    d['ordered_pages'] = ExtendedFlatPage.objects.all()
    return d
