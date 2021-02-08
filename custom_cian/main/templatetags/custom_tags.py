from django import template

from datetime import datetime

from main.models import Saller, Subscriber


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


@register.simple_tag
def is_subscriber(user):
    try:
        return Subscriber.objects.get(user=user)
    except Subscriber.DoesNotExist:
        return
