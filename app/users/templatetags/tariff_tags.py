from django import template

register = template.Library()


@register.filter(name="split_text")
def split_text(value, symbol):
    return value.split(symbol)
