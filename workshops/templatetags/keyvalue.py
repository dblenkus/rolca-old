from django import template

register = template.Library()  # pylint: disable=invalid-name


@register.filter
def keyvalue(dictionary, key):
    return dictionary[key]
