from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def reverse_string(target_string):
    return ''.join(reversed(list(target_string)))
