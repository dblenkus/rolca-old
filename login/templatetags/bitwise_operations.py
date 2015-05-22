from django import template

register = template.Library()  # pylint: disable=invalid-name


@register.filter
def bit_or(value, arg):
    """Bitwise or"""
    return value | arg


@register.filter
def bit_and(value, arg):
    """Bitwise and"""
    return value & arg
