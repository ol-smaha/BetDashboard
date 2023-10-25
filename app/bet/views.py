from datetime import datetime
from django.db.models import Count
from django.views.generic.list import ListView

from .charts import MorrisChartDonut, MorrisChartLine, MorrisChartStacked
from .constants import BET_BASE_TABLE_FIELD_NAMES, BetResultEnum
from .models import BetBase
from django.db.models import Sum
from bet.constants import BetResultEnum


class BetHistoryView(ListView):
    model = BetBase
    template_name = 'bet/bet_history.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        total_bets_count = self.model.objects.all().count()
        total_bets_profit = '+500.00 $'
        total_bets_amount = '7500.00 $'
        total_roi = '+7.5 %'
        context_data = {
            'title': 'Bet History',
            'total_bets_count': total_bets_count,
            'total_bets_profit': total_bets_profit,
            'total_bets_amount': total_bets_amount,
            'total_roi': total_roi,
            'bet_fields': BET_BASE_TABLE_FIELD_NAMES.values(),
            'bets': self.get_queryset(),
        }
        return context_data


class BetGraphsView(ListView):
    model = BetBase
    template_name = 'bet/bet_graphs.html'

    def _get_morris_chart_donut_data(self):
        raw_data = {}
        data = {}
        sorted_results = [BetResultEnum.WIN, BetResultEnum.DRAWN,
                          BetResultEnum.LOSE, BetResultEnum.UNKNOWN]
        objects = (self.get_queryset()
                   .values('result')
                   .annotate(result_count=Count('result'))
                   .order_by())
        for obj in objects:
            raw_data.update({obj.get('result'): obj.get('result_count')})
        for res in sorted_results:
            data.update({res: raw_data.get(res)})
        return data

    def _get_morris_chart_line_data(self):
        data = {}
        raw_data = (self.get_queryset()
                    .values('date_game')
                    .annotate(game_count=Count('date_game'))
                    .order_by('date_game'))
        for dict_data in raw_data:
            date_game = datetime.strftime(dict_data.get('date_game'), '%Y-%m-%d')
            game_count = dict_data.get('game_count')
            data.update({date_game: {'BETS': game_count}})
        return data

    def _get_morris_chart_stacked_data(self):
        data = {}
        raw_data = ((self.get_queryset()
                     .values('result', 'date_game')
                     .annotate(res_count=Count('result'), )
                     .order_by('date_game')))
        for dict_data in raw_data:
            date_game = datetime.strftime(dict_data.get('date_game'), '%Y-%m-%d')
            if not data.get(date_game, {}):
                data[date_game] = {}

            result = dict_data.get('result')
            result_count = dict_data.get('res_count', 0)
            data[date_game][result] = result_count
        return data

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        morris_line_json = MorrisChartLine.to_json_data(self._get_morris_chart_line_data())
        morris_stacked_bar_json = MorrisChartStacked.to_json_data(self._get_morris_chart_stacked_data())
        morris_donut_json = MorrisChartDonut.to_json_data(self._get_morris_chart_donut_data())

        context_data = {
            'morris_line_data': morris_line_json,
            'morris_line_ykeys': '["BETS"]',
            'morris_line_labels': '["BETS"]',
            'morris_stacked_data': morris_stacked_bar_json,
            'morris_stacked_ykeys': f'["{BetResultEnum.WIN}", "{BetResultEnum.DRAWN}", '
                                    f'"{BetResultEnum.LOSE}", "{BetResultEnum.UNKNOWN}"]',
            'morris_stacked_labels': f'["{BetResultEnum.WIN}", "{BetResultEnum.DRAWN}", '
                                     f'"{BetResultEnum.LOSE}", "{BetResultEnum.UNKNOWN}"]',
            'morris_donut_data': morris_donut_json,
            'title': 'Bets Graphs'
        }
        print(context_data)
        return context_data


class Statistic(ListView):
    model = BetBase
    template_name = 'bet/statistic.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        total_bets_count = self.model.objects.all().count()
        total_bets_profit = 7500.00
        total_bets_amount_sum = self.model.objects.aggregate(Sum('amount'))
        total_bets_amount = float(total_bets_amount_sum.get('amount__sum'))
        total_roi = total_bets_profit // total_bets_amount * 100
        res_win = self.model.objects.filter(result=BetResultEnum.WIN).count()
        res_drawn = self.model.objects.filter(result=BetResultEnum.DRAWN).count()
        res_lose = self.model.objects.filter(result=BetResultEnum.LOSE).count()
        res_unknown = self.model.objects.filter(result=BetResultEnum.UNKNOWN).count()

        context_data = {
            'title': 'Bet Statistic',
            'bets': self.get_queryset(),
            'total_bets_count': total_bets_count,
            'total_bets_profit': total_bets_profit,
            'total_bets_amount': total_bets_amount,
            'total_roi': total_roi,
            'res_win': res_win,
            'res_drawn': res_drawn,
            'res_lose': res_lose,
            'res_unknown': res_unknown,

        }
        return context_data
