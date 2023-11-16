from datetime import datetime, date
from pprint import pprint

from dateutil.relativedelta import relativedelta

from django.db.models import Count, Sum, F
from django.forms import HiddenInput
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView
from django.views.generic.list import ListView
from django.utils.timezone import now

from .models import BetBase, BetFootball
from .charts import MorrisChartDonut, MorrisChartLine, MorrisChartStacked, MorrisChartBar
from .constants import BET_BASE_TABLE_FIELD_NAMES, ChartDateType, BET_FOOTBALL_FIELDS_NAMES
from .forms import BetHistoryFilterForm, BetProfitGraphFilterForm, FootballBetHistoryFilterForm, BetCreateForm
from bet.constants import BetResultEnum


class BetHistoryView(ListView):
    model = BetBase
    paginate_by = 50
    template_name = 'bet/bet_history.html'

    def filtered_queryset(self, qs):
        sport_kind_values = self.request.GET.getlist('sport_kind')
        if sport_kind_values:
            qs = qs.filter(sport_kind__name__in=sport_kind_values)

        date_game_start = self.request.GET.get('date_game_start')
        if date_game_start:
            qs = qs.filter(date_game__gte=datetime.strptime(date_game_start, '%m/%d/%Y'))

        date_game_end = self.request.GET.get('date_game_end')
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
            if ordering == 'is_favourite':
                qs = qs.order_by('-is_favourite')
            else:
                qs = qs.order_by(ordering)

        coefficient_min = self.request.GET.get('coefficient_min')
        if coefficient_min:
            qs = qs.filter(coefficient__gte=coefficient_min)

        coefficient_max = self.request.GET.get('coefficient_max')
        if coefficient_max:
            qs = qs.filter(coefficient__lte=coefficient_max)

        return qs

    def base_queryset(self):
        return self.model.objects.all()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetHistoryFilterForm(self.request.GET)
        page_obj = context.get('page_obj')
        page_obj_start = page_obj.number * self.paginate_by - self.paginate_by + 1
        page_obj_end = page_obj.number * self.paginate_by
        page_obj_end = page_obj_end if page_obj_end <= self.get_queryset().count() else self.get_queryset().count()
        page_obj_count_string = f'{page_obj_start} - {page_obj_end} з {self.get_queryset().count()}'
        context.update({
            'title': 'Bet History',
            'bet_fields': BET_BASE_TABLE_FIELD_NAMES.values(),
            'filter_form': filter_form,
            'page_obj_count_string': page_obj_count_string,
            'query_parametes': self.request.GET,
        })
        return context


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
                   .annotate(Count('result'))
                   .order_by())
        for obj in objects[:50]:
            raw_data.update({obj.get('result'): obj.get('result__count')})
        for res in sorted_results:
            data.update({res: raw_data.get(res)})
        return data

    def _get_morris_chart_line_data(self):
        data = {}
        raw_data = (self.get_queryset()
                    .values('date_game')
                    .annotate(game_count=Count('date_game'))
                    .order_by('date_game'))
        for dict_data in raw_data[:50]:
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
        for dict_data in raw_data[:50]:
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

    @staticmethod
    def _process_profit_sum(qs, check_date, data, date_format='%Y-%m-%d'):
        date_str = check_date.strftime(date_format)
        profit = qs.values('profit').aggregate(Sum('profit')).get('profit__sum') or 0.00
        data.update({date_str: {'Прибуток': float(profit), 'К-сть': qs.count()}})

    def _get_profit_all_morris_chart_line_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # всі ставки від найпершої по кожен день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                check_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_profit_sum(qs, check_date, data)

        elif date_type == ChartDateType.LAST_30_DAYS:
            # всі ставки від найпершої по кожен день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                check_date = start_date + relativedelta(days=day)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_profit_sum(qs, check_date, data)

        elif date_type == ChartDateType.MONTHS:
            # всі ставки від найпершої по останній день місяця останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                check_date = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_profit_sum(qs, check_date, data, date_format='%Y-%m')

        elif ChartDateType.YEARS:
            # всі ставки від найпершої по останній день року всіх років
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                check_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_profit_sum(qs, check_date, data, date_format='%Y-%m')

        return data

    def _get_profit_period_morris_chart_bar_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # ставки за кожен окремий день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                check_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__range=[check_date, check_date])
                self._process_profit_sum(qs, check_date, data)

        elif date_type == ChartDateType.LAST_30_DAYS:
            # ставки за кожен окремий день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                check_date = start_date + relativedelta(days=day)
                qs = self.get_queryset().filter(date_game__range=[check_date, check_date])
                self._process_profit_sum(qs, check_date, data)

        elif date_type == ChartDateType.MONTHS:
            # ставки за кожен окремий місяць останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                check_date = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__range=[month_date_start, check_date])
                self._process_profit_sum(qs, check_date, data, date_format='%Y-%m')

        elif ChartDateType.YEARS:
            # ставки за кожен окремий рік
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                start_year_date = date(year=year, month=1, day=1)
                check_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__range=[start_year_date, check_date])
                self._process_profit_sum(qs, check_date, data, date_format='%Y-%m')

        return data

    def filtered_queryset(self, qs):
        sport_kind_values = self.request.GET.getlist('sport_kind')
        if sport_kind_values:
            qs = qs.filter(sport_kind__name__in=sport_kind_values)

        date_game_start = self.request.GET.get('date_game_start')
        if date_game_start:
            qs = qs.filter(date_game__gte=datetime.strptime(date_game_start, '%m/%d/%Y'))

        date_game_end = self.request.GET.get('date_game_end')
        if date_game_end:
            qs = qs.filter(date_game__lte=datetime.strptime(date_game_end, '%m/%d/%Y'))

        amount_min = self.request.GET.get('amount_min')
        if amount_min:
            qs = qs.filter(amount__gte=amount_min)

        amount_max = self.request.GET.get('amount_max')
        if amount_max:
            qs = qs.filter(amount__lte=amount_max)

        coefficient_min = self.request.GET.get('coefficient_min')
        if coefficient_min:
            qs = qs.filter(coefficient__gte=coefficient_min)

        coefficient_max = self.request.GET.get('coefficient_max')
        if coefficient_max:
            qs = qs.filter(coefficient__lte=coefficient_max)

        return qs

    def base_queryset(self):
        return self.model.objects.all()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        filter_form = BetProfitGraphFilterForm

        context_data = {
            'profit_now_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.NOW)),
            'profit_last_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.MONTHS)),
            'profit_year_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.YEARS)),
            'profit_line_ykeys': '["К-сть", "Прибуток"]',
            'profit_line_labels': '["К-сть", "Прибуток"]',

            'profit_now_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.NOW)),
            'profit_last_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.MONTHS)),
            'profit_year_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.YEARS)),
            'profit_bar_ykeys': '["К-сть", "Прибуток"]',
            'profit_bar_labels': '["К-сть", "Прибуток"]',

            'filter_form': filter_form,
            'title': 'Profit Graphs',
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
        total_bets_roi = round(total_bets_profit * 100 / total_bets_amount, 2)

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


class FootballBetHistoryView(ListView):
    model = BetFootball
    template_name = 'bet/bet_football_history.html'

    def filtered_queryset(self, qs):
        date_game_start = self.request.GET.get('date_game_start')
        if date_game_start:
            qs = qs.filter(date_game__gte=datetime.strptime(date_game_start, '%m/%d/%Y'))

        date_game_end = self.request.GET.get('date_game_end')
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

        bet_type = self.request.GET.getlist('bet_type')
        if bet_type:
            qs = qs.filter(bet_type__in=bet_type)

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

        bet_values = self.request.GET.getlist('bet_value')
        if bet_values:
            qs = qs.filter(bet_value__in=bet_values)

        game_status = self.request.GET.getlist('game_status')
        if game_status:
            qs = qs.filter(game_status__in=game_status)

        competition_values = self.request.GET.getlist('competition')
        if competition_values:
            qs = qs.filter(competition__name__in=competition_values)

        return qs

    def base_queryset(self):
        return self.model.objects.filter(sport_kind__name='Футбол')

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        filter_form = FootballBetHistoryFilterForm

        context_data = {
            'title': 'Football Bet History',
            'bets': self.get_queryset()[:50],
            'football_bet_fields': BET_FOOTBALL_FIELDS_NAMES.values(),
            'filter_form': filter_form
        }
        return context_data


class BetGraphsResultView(ListView):
    model = BetBase
    template_name = 'bet/bet_graphs_result.html'

    @staticmethod
    def _process_result_count(qs, check_date, data, date_format='%Y-%m-%d'):
        valid_values = [BetResultEnum.WIN, BetResultEnum.DRAWN, BetResultEnum.LOSE]
        raw_data = qs.values('result').annotate(Count('result'))
        date_str = check_date.strftime(date_format)
        data.update({date_str: {BetResultEnum.WIN: 0, BetResultEnum.DRAWN: 0, BetResultEnum.LOSE: 0}})
        for obj in raw_data:
            if obj.get('result') in valid_values:
                data.get(date_str).update({obj.get('result'): obj.get('result__count')})

    def _get_profit_all_morris_chart_line_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # всі ставки від найпершої по кожен день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                check_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_result_count(qs, check_date, data)

        elif date_type == ChartDateType.LAST_30_DAYS:
            # всі ставки від найпершої по кожен день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                check_date = start_date + relativedelta(days=day)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_result_count(qs, check_date, data)

        elif date_type == ChartDateType.MONTHS:
            # всі ставки від найпершої по останній день місяця останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                check_date = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_result_count(qs, check_date, data, date_format='%Y-%m')

        elif ChartDateType.YEARS:
            # всі ставки від найпершої по останній день року всіх років
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                check_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_result_count(qs, check_date, data, date_format='%Y-%m')

        return data

    def _get_profit_period_morris_chart_bar_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # ставки за кожен окремий день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                check_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__range=[check_date, check_date])
                self._process_result_count(qs, check_date, data)

        elif date_type == ChartDateType.LAST_30_DAYS:
            # ставки за кожен окремий день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                check_date = start_date + relativedelta(days=day)
                qs = self.get_queryset().filter(date_game__range=[check_date, check_date])
                self._process_result_count(qs, check_date, data)

        elif date_type == ChartDateType.MONTHS:
            # ставки за кожен окремий місяць останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                check_date = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__range=[month_date_start, check_date])
                self._process_result_count(qs, check_date, data, date_format='%Y-%m')

        elif ChartDateType.YEARS:
            # ставки за кожен окремий рік
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                start_year_date = date(year=year, month=1, day=1)
                check_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__range=[start_year_date, check_date])
                self._process_result_count(qs, check_date, data, date_format='%Y-%m')

        return data

    def filtered_queryset(self, qs):
        sport_kind_values = self.request.GET.getlist('sport_kind')
        if sport_kind_values:
            qs = qs.filter(sport_kind__name__in=sport_kind_values)

        date_game_start = self.request.GET.get('date_game_start')
        if date_game_start:
            qs = qs.filter(date_game__gte=datetime.strptime(date_game_start, '%m/%d/%Y'))

        date_game_end = self.request.GET.get('date_game_end')
        if date_game_end:
            qs = qs.filter(date_game__lte=datetime.strptime(date_game_end, '%m/%d/%Y'))

        amount_min = self.request.GET.get('amount_min')
        if amount_min:
            qs = qs.filter(amount__gte=amount_min)

        amount_max = self.request.GET.get('amount_max')
        if amount_max:
            qs = qs.filter(amount__lte=amount_max)

        coefficient_min = self.request.GET.get('coefficient_min')
        if coefficient_min:
            qs = qs.filter(coefficient__gte=coefficient_min)

        coefficient_max = self.request.GET.get('coefficient_max')
        if coefficient_max:
            qs = qs.filter(coefficient__lte=coefficient_max)

        return qs

    def base_queryset(self):
        return self.model.objects.all()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        filter_form = BetProfitGraphFilterForm

        context_data = {
            'profit_now_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.NOW)),
            'profit_last_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.MONTHS)),
            'profit_year_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.YEARS)),
            'profit_line_ykeys': f'["{BetResultEnum.WIN}", "{BetResultEnum.DRAWN}", "{BetResultEnum.LOSE}"]',
            'profit_line_labels': f'["{BetResultEnum.WIN}", "{BetResultEnum.DRAWN}", "{BetResultEnum.LOSE}"]',

            'profit_now_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.NOW)),
            'profit_last_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.MONTHS)),
            'profit_year_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.YEARS)),
            'profit_bar_ykeys': f'["{BetResultEnum.WIN}", "{BetResultEnum.DRAWN}", "{BetResultEnum.LOSE}"]',
            'profit_bar_labels': f'["{BetResultEnum.WIN}", "{BetResultEnum.DRAWN}", "{BetResultEnum.LOSE}"]',

            'filter_form': filter_form,
            'title': 'Profit Graphs',
        }
        print(context_data['profit_bar_ykeys'])
        return context_data


class BetGraphsRoiView(ListView):
    model = BetBase
    template_name = 'bet/bet_graphs_roi.html'

    @staticmethod
    def _process_roi_sum(qs, check_date, data, date_format='%Y-%m-%d'):
        date_str = check_date.strftime(date_format)
        values = qs.values('profit', 'amount').aggregate(Sum('profit'), Sum('amount'))
        profit_dec = values.get('profit__sum') or 0.00
        profit = float(profit_dec)
        amount_dec = values.get('amount__sum') or 0.00
        amount = float(amount_dec)
        if amount:
            roi = round(profit * 100 / amount, 2)
        else:
            roi = 0.00
        data.update({date_str: {'ROI': float(roi), 'К-сть': qs.count()}})

    def _get_roi_all_morris_chart_line_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # всі ставки від найпершої по кожен день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                check_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_roi_sum(qs, check_date, data)

        elif date_type == ChartDateType.LAST_30_DAYS:
            # всі ставки від найпершої по кожен день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                check_date = start_date + relativedelta(days=day)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_roi_sum(qs, check_date, data)

        elif date_type == ChartDateType.MONTHS:
            # всі ставки від найпершої по останній день місяця останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                check_date = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_roi_sum(qs, check_date, data, date_format='%Y-%m')

        elif ChartDateType.YEARS:
            # всі ставки від найпершої по останній день року всіх років
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                check_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_roi_sum(qs, check_date, data, date_format='%Y-%m')

        return data

    def _get_roi_period_morris_chart_bar_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # ставки за кожен окремий день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                check_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__range=[check_date, check_date])
                self._process_roi_sum(qs, check_date, data)

        elif date_type == ChartDateType.LAST_30_DAYS:
            # ставки за кожен окремий день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                check_date = start_date + relativedelta(days=day)
                qs = self.get_queryset().filter(date_game__range=[check_date, check_date])
                self._process_roi_sum(qs, check_date, data)

        elif date_type == ChartDateType.MONTHS:
            # ставки за кожен окремий місяць останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                check_date = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__range=[month_date_start, check_date])
                self._process_roi_sum(qs, check_date, data, date_format='%Y-%m')

        elif ChartDateType.YEARS:
            # ставки за кожен окремий рік
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                start_year_date = date(year=year, month=1, day=1)
                check_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__range=[start_year_date, check_date])
                self._process_roi_sum(qs, check_date, data, date_format='%Y-%m')

        return data

    def filtered_queryset(self, qs):
        sport_kind_values = self.request.GET.getlist('sport_kind')
        if sport_kind_values:
            qs = qs.filter(sport_kind__name__in=sport_kind_values)

        date_game_start = self.request.GET.get('date_game_start')
        if date_game_start:
            qs = qs.filter(date_game__gte=datetime.strptime(date_game_start, '%m/%d/%Y'))

        date_game_end = self.request.GET.get('date_game_end')
        if date_game_end:
            qs = qs.filter(date_game__lte=datetime.strptime(date_game_end, '%m/%d/%Y'))

        amount_min = self.request.GET.get('amount_min')
        if amount_min:
            qs = qs.filter(amount__gte=amount_min)

        amount_max = self.request.GET.get('amount_max')
        if amount_max:
            qs = qs.filter(amount__lte=amount_max)

        coefficient_min = self.request.GET.get('coefficient_min')
        if coefficient_min:
            qs = qs.filter(coefficient__gte=coefficient_min)

        coefficient_max = self.request.GET.get('coefficient_max')
        if coefficient_max:
            qs = qs.filter(coefficient__lte=coefficient_max)

        return qs

    def base_queryset(self):
        return self.model.objects.all()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        filter_form = BetProfitGraphFilterForm

        context_data = {
            'roi_now_line_data': MorrisChartLine.to_json_data(
                self._get_roi_all_morris_chart_line_data(date_type=ChartDateType.NOW)),
            'roi_last_line_data': MorrisChartLine.to_json_data(
                self._get_roi_all_morris_chart_line_data(date_type=ChartDateType.LAST_30_DAYS)),
            'roi_month_line_data': MorrisChartLine.to_json_data(
                self._get_roi_all_morris_chart_line_data(date_type=ChartDateType.MONTHS)),
            'roi_year_line_data': MorrisChartLine.to_json_data(
                self._get_roi_all_morris_chart_line_data(date_type=ChartDateType.YEARS)),
            'roi_line_ykeys': '["ROI"]',
            'roi_line_labels': '["К-сть", "ROI"]',

            'roi_now_bar_data': MorrisChartBar.to_json_data(
                self._get_roi_period_morris_chart_bar_data(date_type=ChartDateType.NOW)),
            'roi_last_bar_data': MorrisChartBar.to_json_data(
                self._get_roi_period_morris_chart_bar_data(date_type=ChartDateType.LAST_30_DAYS)),
            'roi_month_bar_data': MorrisChartBar.to_json_data(
                self._get_roi_period_morris_chart_bar_data(date_type=ChartDateType.MONTHS)),
            'roi_year_bar_data': MorrisChartBar.to_json_data(
                self._get_roi_period_morris_chart_bar_data(date_type=ChartDateType.YEARS)),
            'roi_bar_ykeys': '["ROI"]',
            'roi_bar_labels': '["К-сть", "ROI"]',

            'filter_form': filter_form,
            'title': 'ROI Graphs',
        }
        return context_data


class BetCreateView(CreateView):
    form_class = BetCreateForm
    template_name = 'bet/bet_create.html'
    success_url = reverse_lazy('bet_history')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'].fields['user'].initial = self.request.user.pk
        context['form'].fields['user'].widget = HiddenInput()
        return context


class BetBaseChangeFavouriteStatusView(DetailView):
    model = BetBase
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().change_is_favourite()
        return redirect(reverse_lazy('bet_history') + f'?{self.request.GET.urlencode()}')


class BetBaseDeleteView(DetailView):
    model = BetBase
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect(reverse_lazy('bet_history') + f'?{self.request.GET.urlencode()}')
