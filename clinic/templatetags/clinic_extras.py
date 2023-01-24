import datetime

from django import template
from datetime import date

register = template.Library()


@register.filter
def years_to_now(value: date):
    return int((date.today() - value).days // 365.25)


@register.simple_tag
def frmt_datetime(obj: datetime.datetime, frmt_str):
    return obj.strftime(frmt_str)
