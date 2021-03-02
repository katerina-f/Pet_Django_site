from django import template
from django.contrib.auth.models import AnonymousUser

from datetime import datetime

from main.models import Saller, Subscriber
from main.forms import SearchForm


register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.now().strftime(format_string)


@register.simple_tag
def current_saller(user):
    if isinstance(user, AnonymousUser):
        return

    try:
        return Saller.objects.get(created_by=user).id
    except Saller.DoesNotExist:
        return


@register.simple_tag
def is_subscriber(user):
    if isinstance(user, AnonymousUser):
        return

    try:
        return Subscriber.objects.get(user=user)
    except Subscriber.DoesNotExist:
        return


@register.simple_tag
def search_form():
    return SearchForm()
