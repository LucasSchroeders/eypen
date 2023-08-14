from django import template

register = template.Library()


@register.filter
def display_business_area(value):
    value = value.replace('[', '')
    value = value.replace(']', '')
    for v in value:
        if v == '\"':
            value = value.replace('\"', '')
    return value