# novels/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='custom_filter')
def custom_filter(value):
    # Your custom filter logic here
    return value
