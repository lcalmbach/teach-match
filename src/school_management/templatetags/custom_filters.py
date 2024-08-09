import calendar
import datetime
from django import template
from django.contrib.auth.models import Group


register = template.Library()

@register.filter(name='boolean_to_ja_nein')
def boolean_to_ja_nein(value):
    if isinstance(value, bool):
        return "ja" if value else "nein"
    return value

@register.filter
def weekday(value):
    # Assuming `value` is a date or datetime object
    if isinstance(value, (datetime.date, datetime.datetime)):
        return calendar.day_abbr[value.weekday()]
    return ''

@register.filter(name='is_in_group')
def is_in_group(user, group_name):
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False