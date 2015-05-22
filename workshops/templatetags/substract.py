from django import template

register = template.Library()  # pylint: disable=invalid-name


@register.filter
def sub(val1, val2):
    return val1 - val2
