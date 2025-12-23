# templatetags/custom_filters.py
# Create this file in: playground/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    """
    Custom filter to lookup dictionary values in templates
    Usage: {{ my_dict|dict_lookup:my_key }}
    """
    return dictionary.get(key, [])