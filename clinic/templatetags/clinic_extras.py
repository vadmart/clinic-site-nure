import datetime

from django import template
from datetime import date

register = template.Library()


@register.filter
def years_to_now(value: date) -> int:
    return int((date.today() - value).days // 365.25)


@register.simple_tag
def frmt_datetime(obj: datetime.datetime, frmt_str) -> str:
    return obj.strftime(frmt_str)


@register.simple_tag
def uk_pluralize(count: int, words_variants: str) -> str:
    variants = words_variants.split(",")
    if count % 10 == 1 and count % 100 != 11:
        return variants[0]
    elif 2 <= count % 10 <= 4 and not 12 <= count % 100 <= 14:
        return variants[1]
    return variants[2]
