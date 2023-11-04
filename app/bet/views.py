from datetime import datetime, timedelta, date
from pprint import pprint

from dateutil.relativedelta import relativedelta

from django.db.models import Count, Sum
from django.views.generic.list import ListView
from django.utils.timezone import now

from .charts import MorrisChartDonut, MorrisChartLine, MorrisChartStacked, MorrisChartArea
from .constants import BET_BASE_TABLE_FIELD_NAMES, ChartDateType
from .forms import BetHistoryFilterForm
from .models import BetBase
from bet.constants import BetResultEnum


class BetHistoryView(ListView):
    model = BetBase
    template_name = 'bet/bet_history.html'

    def filtered_queryset(self, qs):
        print(" --- 111111 --- ")
        print(self.request.GET)
        
        sport_kind_values = self.request.GET.getlist('sport_kind')
        if sport_kind_values:
            qs = qs.filter(sport_kind__name__in=sport_kind_values)

        date_game_start = self.request.GET.get('dategamestart')
        if date_game_start:
            qs = qs.filter(date_game__gte=datetime.strptime(date_game_start, '%m/%d/%Y'))

        date_game_end = self.request.GET.get('dategameend')
        if date_game_end:
            qs = qs.filter(date_game__lte=datetime.strptime(date_game_end, '%m/%d/%Y'))

        amount_min = self.request.GET.get('amount_min')
        if amount_min:
            qs = qs.filter(amount__gte=amount_min)

        amount_max = self.request.GET.get('amount_max')
        if amount_max:
            qs = qs.filter(amount__lte=amount_max)

        result_value = self.request.GET.getlist('result')
        if result_value:
            qs = qs.filter(result__in=result_value)

        is_favourite_value = self.request.GET.getlist('is_favourite')
        if is_favourite_value:
            qs = qs.filter(is_favourite__in=is_favourite_value)
            
        ordering = self.request.GET.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        coefficient_min = self.request.GET.get('coefficient_min')
        if coefficient_min:
            qs = qs.filter(coefficient__gte=coefficient_min)

        coefficient_max = self.request.GET.get('coefficient_max')
        if coefficient_max:
            qs = qs.filter(coefficient__lte=coefficient_max)

        print(" --- 222222 --- ")
        return qs

    def base_queryset(self):
        return self.model.objects.all()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        filter_form = BetHistoryFilterForm
        context_data = {
            'title': 'Bet History',
            'total_bets_count': self.get_queryset().count(),
            'bet_fields': BET_BASE_TABLE_FIELD_NAMES.values(),
            'filter_form': filter_form,
            'bets': self.get_queryset()[:50],
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
        return context_data


class BetGraphsProfitView(ListView):
    model = BetBase
    template_name = 'bet/bet_graphs_profit.html'

    def _get_profit_all_morris_chart_area_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # всі ставки від найпершої по кожен день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                day_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__lte=day_date)
                profit = qs.values('profit').aggregate(Sum('profit')).get('profit__sum') or 0.00
                data.update({day_date.strftime('%Y-%m-%d'): {'Прибуток': float(profit)}})

        elif date_type == ChartDateType.LAST_30_DAYS:
            # всі ставки від найпершої по кожен день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                day_date = start_date + timedelta(days=day)
                qs = self.get_queryset().filter(date_game__lte=day_date)
                profit = qs.values('profit').aggregate(Sum('profit')).get('profit__sum') or 0.00
                data.update({day_date.strftime('%Y-%m-%d'): {'Прибуток': float(profit)}})

        elif date_type == ChartDateType.MONTHS:
            # всі ставки від найпершої по останній день місяця останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                month_date_end = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__lte=month_date_end)
                profit = qs.values('profit').aggregate(Sum('profit')).get('profit__sum') or 0.00
                data.update({month_date_start.strftime('%Y-%m'): {'Прибуток': float(profit)}})

        elif ChartDateType.YEARS:
            # всі ставки від найпершої по останній день року всіх років
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                end_year_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__lte=end_year_date)
                profit = qs.values('profit').aggregate(Sum('profit')).get('profit__sum') or 0.00
                data.update({year: {'Прибуток': float(profit)}})

        return data

    def _get_profit_period_morris_chart_stacked_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # ставки за кожен окремий день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                day_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__range=[day_date, day_date])
                profit = qs.values('profit').aggregate(Sum('profit')).get('profit__sum') or 0.00
                data.update({day_date.strftime('%Y-%m-%d'): {'Прибуток': float(profit)}})

        elif date_type == ChartDateType.LAST_30_DAYS:
            # ставки за кожен окремий день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                day_date = start_date + timedelta(days=day)
                qs = self.get_queryset().filter(date_game__range=[day_date, day_date])
                profit = qs.values('profit').aggregate(Sum('profit')).get('profit__sum') or 0.00
                data.update({day_date.strftime('%Y-%m-%d'): {'Прибуток': float(profit)}})

        elif date_type == ChartDateType.MONTHS:
            # ставки за кожен окремий місяць останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                month_date_end = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__range=[month_date_start, month_date_end])
                profit = qs.values('profit').aggregate(Sum('profit')).get('profit__sum') or 0.00
                data.update({month_date_start.strftime('%Y-%m'): {'Прибуток': float(profit)}})

        elif ChartDateType.YEARS:
            # ставки за кожен окремий рік
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                start_year_date = date(year=year, month=1, day=1)
                end_year_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__range=[start_year_date, end_year_date])
                profit = qs.values('profit').aggregate(Sum('profit')).get('profit__sum') or 0.00
                data.update({year: {'Прибуток': float(profit)}})

        return data

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context_data = {
            'profit_now_area_data': MorrisChartArea.to_json_data(
                self._get_profit_all_morris_chart_area_data(date_type=ChartDateType.NOW)),
            'profit_last_area_data': MorrisChartArea.to_json_data(
                self._get_profit_all_morris_chart_area_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_area_data': MorrisChartArea.to_json_data(
                self._get_profit_all_morris_chart_area_data(date_type=ChartDateType.MONTHS)),
            'profit_year_area_data': MorrisChartArea.to_json_data(
                self._get_profit_all_morris_chart_area_data(date_type=ChartDateType.YEARS)),
            'profit_area_ykeys': '["Прибуток"]',
            'profit_area_labels': '["Прибуток"]',

            'profit_now_stacked_data': MorrisChartStacked.to_json_data(
                self._get_profit_period_morris_chart_stacked_data(date_type=ChartDateType.NOW)),
            'profit_last_stacked_data': MorrisChartStacked.to_json_data(
                self._get_profit_period_morris_chart_stacked_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_stacked_data': MorrisChartStacked.to_json_data(
                self._get_profit_period_morris_chart_stacked_data(date_type=ChartDateType.MONTHS)),
            'profit_year_stacked_data': MorrisChartStacked.to_json_data(
                self._get_profit_period_morris_chart_stacked_data(date_type=ChartDateType.YEARS)),
            'profit_stacked_ykeys': '["Прибуток"]',
            'profit_stacked_labels': '["Прибуток"]',

            'title': 'Profit Graphs'
        }
        return context_data


class Statistic(ListView):
    model = BetBase
    template_name = 'bet/statistic.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        total_bets_count = self.get_queryset().count()
        total_bets_profit = float(self.get_queryset().aggregate(Sum('profit')).get('profit__sum'))
        total_bets_amount = float(self.get_queryset().aggregate(Sum('amount')).get('amount__sum'))
        total_bets_roi = total_bets_profit * 100 // total_bets_amount

        res_win = self.model.objects.filter(result=BetResultEnum.WIN).count()
        res_drawn = self.model.objects.filter(result=BetResultEnum.DRAWN).count()
        res_lose = self.model.objects.filter(result=BetResultEnum.LOSE).count()
        res_unknown = self.model.objects.filter(result=BetResultEnum.UNKNOWN).count()

        context_data = {
            'title': 'Bet Statistic',
            'total_bets_count': total_bets_count,
            'total_bets_profit': total_bets_profit,
            'total_bets_amount': total_bets_amount,
            'total_bets_roi': total_bets_roi,
            'res_win': res_win,
            'res_drawn': res_drawn,
            'res_lose': res_lose,
            'res_unknown': res_unknown,

        }
        return context_data
