from django import template

from datetime import datetime

from main.models import Saller


register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.now().strftime(format_string)


@register.simple_tag
def current_saller(user):
    try:
        return Saller.objects.get(created_by=user).id
    except Saller.DoesNotExist:
        return
