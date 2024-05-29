from django import template

register = template.Library()

@register.filter(name='boolean_to_ja_nein')
def boolean_to_ja_nein(value):
    if isinstance(value, bool):
        return "ja" if value else "nein"
    return value
