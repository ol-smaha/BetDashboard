from django import template

from bet.constants import BET_FOOTBALL_FIELDS_NAMES, BET_BASE_TABLE_FIELD_NAMES, MENU_TREE, \
    COMPETITION_ORDERING_FIELDS_NAMES, SPORT_KIND_ORDERING_FIELDS_NAMES, BETTING_SERVICE_ORDERING_FIELDS_NAMES
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
def bet_football_ordering_value(value):
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


@register.filter
def competition_ordering_value(value):
    default = 'pk'
    desc_fields = []
    exclude_fields = ['action_delete']
    try:
        ordering = reverse_dict(COMPETITION_ORDERING_FIELDS_NAMES).get(value, '')
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
def sport_kind_ordering_value(value):
    default = 'pk'
    desc_fields = []
    exclude_fields = ['action_delete']
    try:
        ordering = reverse_dict(SPORT_KIND_ORDERING_FIELDS_NAMES).get(value, '')
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
def betting_service_ordering_value(value):
    default = 'pk'
    desc_fields = []
    exclude_fields = ['action_delete']
    try:
        ordering = reverse_dict(BETTING_SERVICE_ORDERING_FIELDS_NAMES).get(value, '')
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
def is_parent_menu_active(parent, child):
    try:
        parents = MENU_TREE.get(child)
        return parent in parents
    except:
        return False


@register.filter
def check_empty(value, default=''):
    return value if value else default

