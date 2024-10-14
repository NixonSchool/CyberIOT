from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by its key."""
    return dictionary.get(key)

@register.filter
def get_attr(obj, attr_name):
    """Get an attribute of an object by its name."""
    return getattr(obj, attr_name, None)
