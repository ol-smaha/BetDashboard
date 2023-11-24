import json
from datetime import datetime, date

from dateutil.relativedelta import relativedelta

from django.db.models import Count, Sum, F, Avg, Min
from django.forms import HiddenInput
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView
from django.utils.timezone import now

from .mixins import BetFilterMixin
from .models import BetBase, BetFootball
from .charts import MorrisChartDonut, MorrisChartLine, MorrisChartStacked, MorrisChartBar, CalendarDashboard
from .constants import BET_BASE_TABLE_FIELD_NAMES, ChartDateType, BET_FOOTBALL_FIELDS_NAMES
from .forms import BetHistoryFilterForm, BetProfitGraphFilterForm, FootballBetHistoryFilterForm, BetCreateForm, \
    BetFootballCreateForm, RatingFilterForm, StatisticFilterForm
from bet.constants import BetResultEnum


class BetHistoryView(BetFilterMixin, ListView):
    model = BetBase
    paginate_by = 50
    template_name = 'bet/bet_history.html'

    def base_queryset(self):
        return self.model.objects.filter(user=self.request.user)

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
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        morris_line_json = MorrisChartLine.to_json_data(self._get_morris_chart_line_data())
        morris_stacked_bar_json = MorrisChartStacked.to_json_data(self._get_morris_chart_stacked_data())
        morris_donut_json = MorrisChartDonut.to_json_data(self._get_morris_chart_donut_data())

        context.update({
            'morris_line_data': morris_line_json,
            'morris_line_ykeys': json.dumps(["BETS"]),
            'morris_line_labels': json.dumps(["BETS"]),
            'morris_stacked_data': morris_stacked_bar_json,
            'morris_stacked_ykeys': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN,
                                                BetResultEnum.LOSE, BetResultEnum.UNKNOWN]),
            'morris_stacked_labels': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN,
                                                BetResultEnum.LOSE, BetResultEnum.UNKNOWN]),
            'morris_donut_data': morris_donut_json,
            'title': 'Bets Graphs'
        })
        return context


class BetGraphsProfitView(BetFilterMixin, ListView):
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

    def base_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetProfitGraphFilterForm(self.request.GET)

        context.update({
            'profit_now_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.NOW)),
            'profit_last_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.MONTHS)),
            'profit_year_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.YEARS)),
            'profit_line_ykeys': json.dumps(["К-сть", "Прибуток"]),
            'profit_line_labels': json.dumps(["К-сть", "Прибуток"]),

            'profit_now_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.NOW)),
            'profit_last_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.MONTHS)),
            'profit_year_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.YEARS)),
            'profit_bar_ykeys': json.dumps(["К-сть", "Прибуток"]),
            'profit_bar_labels': json.dumps(["К-сть", "Прибуток"]),

            'filter_form': filter_form,
            'title': 'Profit Graphs',
        })
        return context


class Statistic(BetFilterMixin, ListView):
    model = BetBase
    template_name = 'bet/statistic.html'

    def base_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = StatisticFilterForm(self.request.GET)
        total_bets_count = self.get_queryset().count()
        total_bets_profit = self.get_queryset().aggregate(Sum('profit')).get('profit__sum') or 0.00
        total_bets_amount = self.get_queryset().aggregate(Sum('amount')).get('amount__sum') or 0.00
        if total_bets_amount > 0:
            total_bets_roi = round(float(total_bets_profit) * 100 / float(total_bets_amount), 2)
        else:
            total_bets_roi = 0.00
        res_win = self.get_queryset().filter(result=BetResultEnum.WIN).count()
        res_drawn = self.get_queryset().filter(result=BetResultEnum.DRAWN).count()
        res_lose = self.get_queryset().filter(result=BetResultEnum.LOSE).count()
        res_unknown = self.get_queryset().filter(result=BetResultEnum.UNKNOWN).count()

        context.update({
            'title': 'Bet Statistic',
            'filter_form': filter_form,
            'total_bets_count': total_bets_count,
            'total_bets_profit': float(total_bets_profit),
            'total_bets_amount': float(total_bets_amount),
            'total_bets_roi': total_bets_roi,
            'res_win': res_win,
            'res_drawn': res_drawn,
            'res_lose': res_lose,
            'res_unknown': res_unknown,

        })
        return context


class FootballBetHistoryView(BetFilterMixin, ListView):
    model = BetFootball
    paginate_by = 50
    template_name = 'bet/bet_football_history.html'

    def base_queryset(self):
        return self.model.objects.filter(sport_kind__name='Футбол', user=self.request.user)

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = FootballBetHistoryFilterForm(self.request.GET)
        page_obj = context.get('page_obj')
        page_obj_start = page_obj.number * self.paginate_by - self.paginate_by + 1
        page_obj_end = page_obj.number * self.paginate_by
        page_obj_end = page_obj_end if page_obj_end <= self.get_queryset().count() else self.get_queryset().count()
        page_obj_count_string = f'{page_obj_start} - {page_obj_end} з {self.get_queryset().count()}'
        context.update({
            'title': 'Football Bet History',
            'total_bets_count': self.get_queryset().count(),
            'football_bet_fields': BET_FOOTBALL_FIELDS_NAMES.values(),
            'filter_form': filter_form,
            'bets': self.get_queryset()[:50],
            'page_obj_count_string': page_obj_count_string,
            'query_parametes': self.request.GET,
        })
        return context


class BetGraphsResultView(BetFilterMixin, ListView):
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

    def base_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetProfitGraphFilterForm(self.request.GET)

        context.update({
            'profit_now_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.NOW)),
            'profit_last_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.MONTHS)),
            'profit_year_line_data': MorrisChartLine.to_json_data(
                self._get_profit_all_morris_chart_line_data(date_type=ChartDateType.YEARS)),
            'profit_line_ykeys': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN, BetResultEnum.LOSE]),
            'profit_line_labels': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN, BetResultEnum.LOSE]),

            'profit_now_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.NOW)),
            'profit_last_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.MONTHS)),
            'profit_year_bar_data': MorrisChartBar.to_json_data(
                self._get_profit_period_morris_chart_bar_data(date_type=ChartDateType.YEARS)),
            'profit_bar_ykeys': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN, BetResultEnum.LOSE]),
            'profit_bar_labels': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN, BetResultEnum.LOSE]),

            'filter_form': filter_form,
            'title': 'Profit Graphs',
        })
        return context


class BetGraphsRoiView(BetFilterMixin, ListView):
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

    def base_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetProfitGraphFilterForm(self.request.GET)

        context.update({
            'roi_now_line_data': MorrisChartLine.to_json_data(
                self._get_roi_all_morris_chart_line_data(date_type=ChartDateType.NOW)),
            'roi_last_line_data': MorrisChartLine.to_json_data(
                self._get_roi_all_morris_chart_line_data(date_type=ChartDateType.LAST_30_DAYS)),
            'roi_month_line_data': MorrisChartLine.to_json_data(
                self._get_roi_all_morris_chart_line_data(date_type=ChartDateType.MONTHS)),
            'roi_year_line_data': MorrisChartLine.to_json_data(
                self._get_roi_all_morris_chart_line_data(date_type=ChartDateType.YEARS)),
            'roi_line_ykeys': json.dumps(["ROI"]),
            'roi_line_labels': json.dumps(["ROI"]),

            'roi_now_bar_data': MorrisChartBar.to_json_data(
                self._get_roi_period_morris_chart_bar_data(date_type=ChartDateType.NOW)),
            'roi_last_bar_data': MorrisChartBar.to_json_data(
                self._get_roi_period_morris_chart_bar_data(date_type=ChartDateType.LAST_30_DAYS)),
            'roi_month_bar_data': MorrisChartBar.to_json_data(
                self._get_roi_period_morris_chart_bar_data(date_type=ChartDateType.MONTHS)),
            'roi_year_bar_data': MorrisChartBar.to_json_data(
                self._get_roi_period_morris_chart_bar_data(date_type=ChartDateType.YEARS)),
            'roi_bar_ykeys': json.dumps(["ROI"]),
            'roi_bar_labels': json.dumps(["ROI"]),

            'filter_form': filter_form,
            'title': 'ROI Graphs',
        })
        return context


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

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        self.get_object().change_is_favourite()
        return redirect(reverse_lazy('bet_history') + f'?{self.request.GET.urlencode()}')


class BetBaseDeleteView(DetailView):
    model = BetBase
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect(reverse_lazy('bet_history') + f'?{self.request.GET.urlencode()}')


class BetFootballCreateView(CreateView):
    form_class = BetFootballCreateForm
    template_name = 'bet/bet_football_create.html'
    success_url = reverse_lazy('football_history')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'].fields['user'].initial = self.request.user.pk
        context['form'].fields['user'].widget = HiddenInput()
        return context


class BetFootballChangeFavouriteStatusView(DetailView):
    model = BetFootball
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().change_is_favourite()
        return redirect(reverse_lazy('football_history') + f'?{self.request.GET.urlencode()}')


class BetFootballDeleteView(DetailView):
    model = BetFootball
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect(reverse_lazy('football_history') + f'?{self.request.GET.urlencode()}')


class BetGraphsAvgAmountView(BetFilterMixin, ListView):
    model = BetBase
    template_name = 'bet/bet_graphs_amount.html'

    @staticmethod
    def _process_amount_avg(qs, check_date, data, date_format='%Y-%m-%d'):
        date_str = check_date.strftime(date_format)
        amount = round(qs.values('amount').aggregate(Avg('amount')).get('amount__avg') or 0.00, 2)
        data.update({date_str: {'Середня ставка': float(amount), 'К-сть': qs.count()}})

    def _get_amount_all_morris_chart_line_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # всі ставки від найпершої по кожен день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                check_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_amount_avg(qs, check_date, data)

        elif date_type == ChartDateType.LAST_30_DAYS:
            # всі ставки від найпершої по кожен день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                check_date = start_date + relativedelta(days=day)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_amount_avg(qs, check_date, data)

        elif date_type == ChartDateType.MONTHS:
            # всі ставки від найпершої по останній день місяця останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                check_date = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_amount_avg(qs, check_date, data, date_format='%Y-%m')

        elif ChartDateType.YEARS:
            # всі ставки від найпершої по останній день року всіх років
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                check_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__lte=check_date)
                self._process_amount_avg(qs, check_date, data, date_format='%Y-%m')

        return data

    def _get_amount_period_morris_chart_bar_data(self, date_type=ChartDateType.NOW):
        data = {}

        if date_type == ChartDateType.NOW:
            # ставки за кожен окремий день поточного місяця
            now_date = now().date()
            for day in range(1, now_date.day+1):
                check_date = now_date.replace(day=day)
                qs = self.get_queryset().filter(date_game__range=[check_date, check_date])
                self._process_amount_avg(qs, check_date, data)

        elif date_type == ChartDateType.LAST_30_DAYS:
            # ставки за кожен окремий день останніх 30 днів
            start_date = now() - relativedelta(days=30)
            for day in range(0, 31):
                check_date = start_date + relativedelta(days=day)
                qs = self.get_queryset().filter(date_game__range=[check_date, check_date])
                self._process_amount_avg(qs, check_date, data)

        elif date_type == ChartDateType.MONTHS:
            # ставки за кожен окремий місяць останніх 12 місяців
            start_date = now() - relativedelta(years=1)
            start_date = start_date.replace(day=1)
            for month in range(1, 13):
                month_date_start = start_date + relativedelta(months=month)
                check_date = month_date_start + relativedelta(months=1) - relativedelta(days=1)
                qs = self.get_queryset().filter(date_game__range=[month_date_start, check_date])
                self._process_amount_avg(qs, check_date, data, date_format='%Y-%m')

        elif ChartDateType.YEARS:
            # ставки за кожен окремий рік
            earliest_bet = self.get_queryset().earliest('date_game')
            start_year = earliest_bet.date_game.year
            end_year = now().year

            for year in range(start_year, end_year+1):
                start_year_date = date(year=year, month=1, day=1)
                check_date = date(year=year, month=12, day=31)
                qs = self.get_queryset().filter(date_game__range=[start_year_date, check_date])
                self._process_amount_avg(qs, check_date, data, date_format='%Y-%m')

        return data

    def base_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetProfitGraphFilterForm(self.request.GET)

        context.update({
            'amount_now_line_data': MorrisChartLine.to_json_data(
                self._get_amount_all_morris_chart_line_data(date_type=ChartDateType.NOW)),
            'amount_last_line_data': MorrisChartLine.to_json_data(
                self._get_amount_all_morris_chart_line_data(date_type=ChartDateType.LAST_30_DAYS)),
            'amount_month_line_data': MorrisChartLine.to_json_data(
                self._get_amount_all_morris_chart_line_data(date_type=ChartDateType.MONTHS)),
            'amount_year_line_data': MorrisChartLine.to_json_data(
                self._get_amount_all_morris_chart_line_data(date_type=ChartDateType.YEARS)),
            'amount_line_ykeys': json.dumps(["К-сть", "Середня ставка"]),
            'amount_line_labels': '["К-сть", "Середня ставка"]',

            'amount_now_bar_data': MorrisChartBar.to_json_data(
                self._get_amount_period_morris_chart_bar_data(date_type=ChartDateType.NOW)),
            'amount_last_bar_data': MorrisChartBar.to_json_data(
                self._get_amount_period_morris_chart_bar_data(date_type=ChartDateType.LAST_30_DAYS)),
            'amount_month_bar_data': MorrisChartBar.to_json_data(
                self._get_amount_period_morris_chart_bar_data(date_type=ChartDateType.MONTHS)),
            'amount_year_bar_data': MorrisChartBar.to_json_data(
                self._get_amount_period_morris_chart_bar_data(date_type=ChartDateType.YEARS)),
            'amount_bar_ykeys': json.dumps(["К-сть", "Середня ставка"]),
            'amount_bar_labels': json.dumps(["К-сть", "Середня ставка"]),

            'filter_form': filter_form,
            'title': 'Amount Graphs',
        })
        return context


class RatingGraphsView(BetFilterMixin, ListView):
    model = BetFootball
    template_name = 'bet/rating.html'

    def _get_competition_values(self):
        values = []
        for val in self.get_queryset().values_list('competition__name', flat=True).distinct():
            val = val if val is not None else 'Інше'
            values.append(val)
        return values

    def _process_rating_profit_from_competition(self):
        data = {}
        qs = (self.get_queryset()
              .values('competition__name')
              .annotate(profit=Sum('profit'))
              .order_by('-profit'))

        for element in qs:
            competition = element.get('competition__name') or 'Інше'
            profit = element.get('profit') or 0.00
            data.update({
                competition: {
                    'Профіт': round(float(profit), 2),
                }
            })
        return data

    def _process_rating_roi_from_competition(self):
        data = {}
        qs = (self.get_queryset()
              .values('competition__name')
              .annotate(profit_sum=Sum('profit'), amount_sum=Sum('amount'))
              .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
              .order_by('-roi'))

        for element in qs:
            competition = element.get('competition__name') or 'Інше'
            data.update({
                competition: {
                    'ROI': round(float(element.get('roi')), 2),
                }
            })
        return data

    def _process_rating_profit_from_bet_type(self):
        data = {}
        qs = (self.get_queryset()
              .values('bet_type')
              .annotate(profit=Sum('profit'))
              .order_by('-profit'))

        for element in qs:
            bet_type = element.get('bet_type')
            profit = element.get('profit') or 0.00
            data.update({
                bet_type: {
                    'Профіт': round(float(profit), 2),
                }
            })
        return data

    def _process_rating_roi_from_bet_type(self):
        data = {}
        qs = (self.get_queryset()
              .values('bet_type')
              .annotate(profit_sum=Sum('profit'), amount_sum=Sum('amount'))
              .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
              .order_by('-roi'))
        for element in qs:
            bet_type = element.get('bet_type')
            data.update({
                bet_type: {
                    'ROI': round(float(element.get('roi')), 2),
                }
            })
        return data

    def _process_rating_profit_from_sport_kind(self):
        data = {}
        qs = (self.get_queryset()
              .values('sport_kind__name')
              .annotate(profit=Sum('profit'))
              .order_by('-profit'))
        for element in qs:
            sport_kind = element.get('sport_kind__name') or 'Інше'
            profit = element.get('profit') or 0.00
            data.update({
                sport_kind: {
                    'Профіт': round(float(profit), 2),
                }
            })
        return data

    def _process_rating_roi_from_sport_kind(self):
        data = {}
        qs = (self.get_queryset()
              .values('sport_kind__name')
              .annotate(profit_sum=Sum('profit'), amount_sum=Sum('amount'))
              .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
              .order_by('-roi'))
        for element in qs:
            sport_kind = element.get('sport_kind__name') or 'Інше'
            data.update({
                sport_kind: {
                    'ROI': round(float(element.get('roi')), 2),
                }
            })
        return data

    def base_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        filter_form = RatingFilterForm(self.request.GET)

        context.update({
            'title': 'Rating',
            'filter_form': filter_form,
            'profit_by_competition_labels': json.dumps(['Профіт']),
            'profit_by_competition_ykeys': json.dumps(['Профіт']),
            'profit_by_competition_data': MorrisChartBar.to_json_data(
                self._process_rating_profit_from_competition()),
            'roi_by_competition_labels': json.dumps(['ROI']),
            'roi_by_competition_ykeys': json.dumps(['ROI']),
            'roi_by_competition_data': MorrisChartBar.to_json_data(
                self._process_rating_roi_from_competition()),

            'profit_by_bet_type_labels': json.dumps(['Профіт']),
            'profit_by_bet_type_ykeys': json.dumps(['Профіт']),
            'profit_by_bet_type_data': MorrisChartBar.to_json_data(
                self._process_rating_profit_from_bet_type()),
            'roi_by_bet_type_labels': json.dumps(['ROI']),
            'roi_by_bet_type_ykeys': json.dumps(['ROI']),
            'roi_by_bet_type_data': MorrisChartBar.to_json_data(
                self._process_rating_roi_from_bet_type()),

            'profit_by_sport_kind_labels': json.dumps(['Профіт']),
            'profit_by_sport_kind_ykeys': json.dumps(['Профіт']),
            'profit_by_sport_kind_data': MorrisChartBar.to_json_data(
                self._process_rating_profit_from_sport_kind()),
            'roi_by_sport_kind_labels': json.dumps(['ROI']),
            'roi_by_sport_kind_ykeys': json.dumps(['ROI']),
            'roi_by_sport_kind_data': MorrisChartBar.to_json_data(
                self._process_rating_roi_from_sport_kind()),
        })

        return context


class CalendarView(ListView):
    model = BetBase
    template_name = 'bet/calendar.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def _prepare_calendar_data(self):
        data = {}
        start_date = self.get_queryset().values('date_game').aggregate(min_date=Min('date_game')).get('min_date')
        end_date = now().date()
        qs = self.get_queryset().filter(date_game__range=[start_date, end_date]).order_by('date_game', 'result')

        for obj in qs:
            date_str = datetime.strftime(obj.date_game, '%Y-%m-%d')
            inner_dict = {
                'result': obj.result,
                'amount': obj.amount,
                'coefficient': obj.coefficient,
                'profit': obj.profit,
            }
            if data.get(date_str):
                data[date_str].append(inner_dict)
            else:
                data[date_str] = [inner_dict]

        return data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({
            'calendar_data': CalendarDashboard.to_json_data(self._prepare_calendar_data()),
            'date_now': json.dumps(datetime.strftime(now().date(), '%Y-%m-%d'))
        })
        return context
