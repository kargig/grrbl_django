from django import template

register = template.Library()

@register.filter
def class_name(arg):
    return arg.__class__.__name__
