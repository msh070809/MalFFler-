from django import template

register = template.Library()

@register.filter
def split_string(value, delimiter="@"):
    return value.split(delimiter)


@register.filter
def reverse_list(value):
    return list(reversed(value))