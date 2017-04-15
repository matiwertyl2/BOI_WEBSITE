from django import template
from django.template import Template, Context
from ..models import Country

register = template.Library()


@register.filter()
def country_url(value):
    try:
        context = Context({'c': Country.objects.get(name=value)})
        return Template(
            '<img class="flag" src="/static/flags/{{c.code}}.gif">' +
            ' <a href="{% url \'country\' c.code %}">{{ c.name }}</a>'
            ).render(context)
    except Country.DoesNotExist:
        return value


@register.filter()
def award(value, name=False):
    try:
        color = value.split(" ")[0]
        tem = '<img src="/static/olymp/'+color+'.png">'
        if name:
            tem += " "+value
        return Template(tem).render(Context())
    except AttributeError:
        return ""
