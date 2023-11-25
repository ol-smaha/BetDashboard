from django import template

from bet.constants import BET_FOOTBALL_FIELDS_NAMES, BET_BASE_TABLE_FIELD_NAMES
from bet.utils import reverse_dict

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.filter
def bet_base_ordering_value(value):
    default = 'pk'
    desc_fields = ['is_favourite']
    exclude_fields = ['action_delete']
    try:
        ordering = reverse_dict(BET_BASE_TABLE_FIELD_NAMES).get(value, '')
        if ordering not in exclude_fields:
            if ordering in desc_fields:
                return f"-{ordering}"
            else:
                return f"{ordering}"
        else:
            return default
    except:
        return default


@register.filter
def bet_football_ordering_value(value, **kwargs):
    default = 'pk'
    desc_fields = ['is_favourite']
    exclude_fields = ['action_delete']
    try:
        ordering = reverse_dict(BET_FOOTBALL_FIELDS_NAMES).get(value, '')
        if ordering not in exclude_fields:
            if ordering in desc_fields:
                return f"-{ordering}"
            else:
                return f"{ordering}"
        else:
            return default
    except:
        return default
