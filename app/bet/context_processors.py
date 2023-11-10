import json

from bet.constants import BET_RESULT_COLORS, CHART_ONE_LINE_WITH_COUNT_COLORS, CHART_ONE_LINE_COLORS


def graph_colors(request):
    return {
        'chart_one_line_colors': json.dumps(CHART_ONE_LINE_COLORS),
        'chart_one_line_with_count_colors': json.dumps(CHART_ONE_LINE_WITH_COUNT_COLORS),
        'result_colors': json.dumps(BET_RESULT_COLORS)
    }


