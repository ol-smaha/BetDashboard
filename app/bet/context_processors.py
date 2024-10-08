import json

from django.urls import reverse_lazy

from bet.constants import BET_RESULT_COLORS, CHART_ONE_LINE_WITH_COUNT_COLORS, CHART_ONE_LINE_COLORS
from users.models import Notification


def graph_colors(request):
    return {
        'chart_one_line_colors': json.dumps(CHART_ONE_LINE_COLORS),
        'chart_one_line_with_count_colors': json.dumps(CHART_ONE_LINE_WITH_COUNT_COLORS),
        'result_colors': json.dumps(BET_RESULT_COLORS)
    }


def urls(request):
    return {
        'bet_create_url': request.build_absolute_uri(reverse_lazy('bet_create')),
        'bet_football_create_url': request.build_absolute_uri(reverse_lazy('bet_football_create')),

        'json_bet_create_url_for_calendar': json.dumps("https://betoffice.fun/bet/create/"),
        'json_bet_football_create_url': json.dumps(request.build_absolute_uri(reverse_lazy('bet_football_create'))),
    }


def get_notification(request):
    context = {}
    objects = Notification.objects.filter(user=request.user.id, is_active=True)
    context.update({
        'notifications': objects
    })
    return context
