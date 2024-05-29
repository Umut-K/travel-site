from django import template

register = template.Library()

@register.filter
def to_int(value):
    return int(value)

@register.simple_tag
def generate_range(value):
    return range(1, value + 1)

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})