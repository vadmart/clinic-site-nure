from django import template
from datetime import date

register = template.Library()

@register.filter
def years_to_now(value: date):
    return int((date.today() - value).days // 365.25)
