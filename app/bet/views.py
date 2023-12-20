import json
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AnonymousUser

from django.db.models import Count, Sum, F, Avg, Min, Case, Window, When, IntegerField, Q
from django.db.models.functions import TruncMonth, TruncYear
from django.forms import HiddenInput
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView
from django.utils.timezone import now

from .mixins import BetFilterMixin
from .models import BetBase, BetFootball, CompetitionBase, SportKind, BettingService
from .charts import MorrisChartDonut, MorrisChartLine, MorrisChartStacked, MorrisChartBar, CalendarDashboard
from .constants import BET_BASE_TABLE_FIELD_NAMES, ChartDateType, BET_FOOTBALL_FIELDS_NAMES, \
    COMPETITION_RATING_TABLE_FIELD_NAMES, BetFootballTypeEnum, SPORT_KIND_RATING_TABLE_FIELD_NAMES, \
    BET_TYPE_RATING_TABLE_FIELD_NAMES, ChartType
from .forms import BetHistoryFilterForm, BetProfitGraphFilterForm, FootballBetHistoryFilterForm, BetCreateForm, \
    BetFootballCreateForm, RatingFilterForm, StatisticFilterForm, CompetitionCreateForm, ServiceCreateForm, \
    SportKindCreateForm
from bet.constants import BetResultEnum
from .utils import reverse_dict


class BetHistoryView(BetFilterMixin, ListView):
    model = BetBase
    paginate_by = 50
    template_name = 'bet/bet_history.html'

    def base_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return (self.model.objects.filter(user=self.request.user).order_by('-date_game', '-id')
                    .select_related('sport_kind', 'betting_service'))
        return self.model.objects.none()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset()).select_related('sport_kind', 'betting_service')
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetHistoryFilterForm(self.request.GET)
        filter_form.fields['sport_kind'].choices = SportKind.name_choices()
        filter_form.fields['betting_service'].choices = BettingService.name_choices()

        create_form = BetCreateForm()
        create_form.fields['user'].initial = self.request.user.pk
        create_form.fields['user'].widget = HiddenInput()
        create_form.fields['sport_kind'].choices = SportKind.name_choices()
        create_form.fields['betting_service'].choices = BettingService.name_choices()

        page_obj = context.get('page_obj')
        page_obj_start = page_obj.number * self.paginate_by - self.paginate_by + 1
        page_obj_end = page_obj.number * self.paginate_by
        page_obj_end = page_obj_end if page_obj_end <= self.get_queryset().count() else self.get_queryset().count()
        page_obj_count_string = f'{page_obj_start} - {page_obj_end} з {self.get_queryset().count()}'

        context.update({
            'title': 'Загальна історія',
            'menu_key': 'bet_list',
            'bet_fields': BET_BASE_TABLE_FIELD_NAMES.values(),
            'filter_form': filter_form,
            'create_form': create_form,
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
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

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

    def _get_chart_queryset(self, chart_type=ChartType.LINE, date_type=ChartDateType.NOW):
        qs_now_line = (self.get_queryset()
                           .filter(date_game__lte=now().date())
                           .distinct('date_game')
                           .annotate(profit_sum=Window(
                                         expression=Sum("profit"),
                                         partition_by=None,
                                         order_by="date_game"),
                                     count=Window(
                                         expression=Count("pk"),
                                         partition_by=None,
                                         order_by="date_game"))
                           .values('date_game', 'profit_sum', 'count')
                           .order_by('date_game'))

        qs_now_bar = (self.get_queryset()
                          .distinct('date_game')
                          .filter(date_game__range=[now().date().replace(day=1), now().date()])
                          .annotate(profit_sum=Window(
                                        expression=Sum("profit"),
                                        partition_by=F("date_game"),
                                        order_by="date_game"),
                                    count=Window(
                                        expression=Count("pk"),
                                        partition_by=F("date_game"),
                                        order_by="date_game"))
                          .values('date_game', 'profit_sum', 'count')
                          .order_by('date_game'))

        qs_last_line = (self.get_queryset()
                            .filter(date_game__lte=now().date())
                            .distinct('date_game')
                            .annotate(profit_sum=Window(
                                         expression=Sum("profit"),
                                         partition_by=None,
                                         order_by="date_game"),
                                      count=Window(
                                         expression=Count("pk"),
                                         partition_by=None,
                                         order_by="date_game"))
                            .values('date_game', 'profit_sum', 'count')
                            .order_by('date_game'))

        qs_last_bar = (self.get_queryset()
                           .distinct('date_game')
                           .filter(date_game__range=[now().date() - relativedelta(days=30), now().date()])
                           .annotate(profit_sum=Window(
                                         expression=Sum("profit"),
                                         partition_by=F("date_game"),
                                         order_by="date_game"),
                                     count=Window(
                                         expression=Count("pk"),
                                         partition_by=F("date_game"),
                                         order_by="date_game"))
                           .values('date_game', 'profit_sum', 'count')
                           .order_by('date_game'))

        qs_months_line = (self.get_queryset()
                              .filter(date_game__lte=now().date())
                              .annotate(month=TruncMonth('date_game'))
                              .distinct('date_game')
                              .annotate(profit_sum=Window(
                                            expression=Sum("profit"),
                                            partition_by=None,
                                            order_by="month"),
                                        count=Window(
                                            expression=Count("pk"),
                                            partition_by=None,
                                            order_by="month"))
                              .values('date_game', 'profit_sum', 'count')
                              .order_by('date_game'))

        qs_months_bar = (self.get_queryset()
                             .filter(date_game__lte=now().date())
                             .annotate(month=TruncMonth('date_game'))
                             .distinct('date_game')
                             .annotate(profit_sum=Window(
                                           expression=Sum("profit"),
                                           partition_by='month',
                                           order_by="month"),
                                       count=Window(
                                           expression=Count("pk"),
                                           partition_by='month',
                                           order_by="month"))
                             .values('date_game', 'profit_sum', 'count')
                             .order_by('date_game'))

        qs_years_line = (self.get_queryset()
                             .filter(date_game__lte=now().date())
                             .annotate(year=TruncYear('date_game'))
                             .distinct('date_game')
                             .annotate(profit_sum=Window(
                                           expression=Sum("profit"),
                                           partition_by=None,
                                           order_by="year"),
                                       count=Window(
                                           expression=Count("pk"),
                                           partition_by=None,
                                           order_by="year"))
                             .values('date_game', 'profit_sum', 'count')
                             .order_by('date_game'))

        qs_years_bar = (self.get_queryset()
                            .filter(date_game__lte=now().date())
                            .annotate(year=TruncYear('date_game'))
                            .distinct('date_game')
                            .annotate(profit_sum=Window(
                                          expression=Sum("profit"),
                                          partition_by='year',
                                          order_by="year"),
                                      count=Window(
                                          expression=Count("pk"),
                                          partition_by='year',
                                          order_by="year"))
                            .values('date_game', 'profit_sum', 'count')
                            .order_by('date_game'))

        qs = self.model.objects.none()    # імітація пустого queryset

        if chart_type == ChartType.LINE:
            if date_type == ChartDateType.NOW:
                qs = qs_now_line
            elif date_type == ChartDateType.LAST_30_DAYS:
                qs = qs_last_line
            elif date_type == ChartDateType.MONTHS:
                qs = qs_months_line
            elif date_type == ChartDateType.YEARS:
                qs = qs_years_line
        elif chart_type == ChartType.BAR:
            if date_type == ChartDateType.NOW:
                qs = qs_now_bar
            elif date_type == ChartDateType.LAST_30_DAYS:
                qs = qs_last_bar
            elif date_type == ChartDateType.MONTHS:
                qs = qs_months_bar
            elif date_type == ChartDateType.YEARS:
                qs = qs_years_bar

        return qs

    def _get_chart_data(self, chart_type=ChartType.LINE, date_type=ChartDateType.NOW, date_format='%Y-%m-%d'):
        data = {}
        qs = self._get_chart_queryset(chart_type, date_type)

        graph_start_date = None
        if date_type == ChartDateType.NOW:
            graph_start_date = now().date().replace(day=1)
        elif date_type == ChartDateType.LAST_30_DAYS:
            graph_start_date = now().date() - relativedelta(days=30)

        for elem in qs:
            day_date = elem.get('date_game')
            if graph_start_date and day_date < graph_start_date:
                continue
            date_str = day_date.strftime(date_format)
            profit = elem.get('profit_sum', 0.00)
            count = elem.get('count', 0)
            data.update({date_str: {'Прибуток': round(float(profit), 2), 'count': count}})
        return data

    def base_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetProfitGraphFilterForm(self.request.GET)
        filter_form.fields['sport_kind'].choices = SportKind.name_choices()
        filter_form.fields['betting_service'].choices = BettingService.name_choices()

        context.update({
            'profit_last_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.MONTHS, date_format='%Y-%m')),
            'profit_year_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.YEARS, date_format='%Y')),
            'profit_line_ykeys': json.dumps(["Прибуток"]),
            'profit_line_labels': json.dumps(["Прибуток"]),

            'profit_last_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.MONTHS, date_format='%Y-%m')),
            'profit_year_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.YEARS, date_format='%Y')),
            'profit_bar_ykeys': json.dumps(["Прибуток"]),
            'profit_bar_labels': json.dumps(["Прибуток"]),

            'filter_form': filter_form,
            'title': 'Прибутковість',
            'menu_key': 'bet_graphs_profit',
        })

        return context


class Statistic(BetFilterMixin, ListView):
    model = BetBase
    template_name = 'bet/statistic.html'

    def base_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = StatisticFilterForm(self.request.GET)
        filter_form.fields['sport_kind'].choices = SportKind.name_choices()
        filter_form.fields['betting_service'].choices = BettingService.name_choices()

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
            'title': 'Статистика',
            'menu_key': 'bet_statistic',
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
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return (self.model.objects.filter(sport_kind__name='Футбол', user=self.request.user)
                    .order_by('-date_game', '-id')
                    .select_related('sport_kind', 'betting_service', 'team_home', 'team_guest', 'competition'))
        return self.model.objects.none()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset()).select_related('team_home', 'team_guest',
                                                                                  'competition')
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = FootballBetHistoryFilterForm(self.request.GET)
        filter_form.fields['competition'].choices = CompetitionBase.name_choices()
        filter_form.fields['betting_service'].choices = BettingService.name_choices()

        create_form = BetFootballCreateForm()
        create_form.fields['user'].initial = self.request.user.pk
        create_form.fields['user'].widget = HiddenInput()
        create_form.fields['competition'].choices = CompetitionBase.name_choices()
        create_form.fields['betting_service'].choices = BettingService.name_choices()

        page_obj = context.get('page_obj')
        page_obj_start = page_obj.number * self.paginate_by - self.paginate_by + 1
        page_obj_end = page_obj.number * self.paginate_by
        page_obj_end = page_obj_end if page_obj_end <= self.get_queryset().count() else self.get_queryset().count()
        page_obj_count_string = f'{page_obj_start} - {page_obj_end} з {self.get_queryset().count()}'

        context.update({
            'title': 'Історія Футбол',
            'menu_key': 'bet_football_list',
            'total_bets_count': self.get_queryset().count(),
            'football_bet_fields': BET_FOOTBALL_FIELDS_NAMES.values(),
            'filter_form': filter_form,
            'create_form': create_form,
            'page_obj_count_string': page_obj_count_string,
            'query_parametes': self.request.GET,
        })

        return context


class BetGraphsResultView(BetFilterMixin, ListView):
    model = BetBase
    template_name = 'bet/bet_graphs_result.html'

    @staticmethod
    def _cumulative_result_counts(qs, date_field='date_game'):
        list_data = []
        dict_data = {}
        count_win = 0
        count_drawn = 0
        count_lose = 0

        for el in qs:
            count_win += el.get('count_win', 0)
            count_drawn += el.get('count_drawn', 0)
            count_lose += el.get('count_lose', 0)

            result_dict = {
                BetResultEnum.WIN: count_win,
                BetResultEnum.DRAWN: count_drawn,
                BetResultEnum.LOSE: count_lose,
            }
            dict_data[el.get(date_field)] = result_dict

        for day, inner_dict in dict_data.items():
            for result, count in inner_dict.items():
                list_data.append({
                    'date_game': day,
                    'result': result,
                    'count': count,
                })

        return list_data

    @staticmethod
    def _structure_bars(qs, date_field='date_game'):
        data = []
        for el in qs:
            data.append({
                'date_game': el.get(date_field),
                'result': BetResultEnum.WIN,
                'count': el.get('count_win'),
            })
            data.append({
                'date_game': el.get(date_field),
                'result': BetResultEnum.DRAWN,
                'count': el.get('count_drawn'),
            })
            data.append({
                'date_game': el.get(date_field),
                'result': BetResultEnum.LOSE,
                'count': el.get('count_lose'),
            })
        return data

    def _get_chart_queryset(self, chart_type=ChartType.LINE, date_type=ChartDateType.NOW):
        qs_now_line_raw = (self.get_queryset()
                           .filter(date_game__lte=now().date())
                           .values('date_game')
                           .annotate(count_win=Count('pk', filter=Q(result=BetResultEnum.WIN)),
                                     count_drawn=Count('pk', filter=Q(result=BetResultEnum.DRAWN)),
                                     count_lose=Count('pk', filter=Q(result=BetResultEnum.LOSE)),)
                           .order_by('date_game'))
        qs_now_line = self._cumulative_result_counts(qs_now_line_raw)

        qs_now_bar_raw = (self.get_queryset()
                              .filter(date_game__range=[now().date().replace(day=1), now().date()])
                              .values('date_game')
                              .annotate(count_win=Count('pk', filter=Q(result=BetResultEnum.WIN)),
                                        count_drawn=Count('pk', filter=Q(result=BetResultEnum.DRAWN)),
                                        count_lose=Count('pk', filter=Q(result=BetResultEnum.LOSE)), )
                              .order_by('date_game'))
        qs_now_bar = self._structure_bars(qs_now_bar_raw)

        qs_last_line_raw = (self.get_queryset()
                                .filter(date_game__lte=now().date())
                                .values('date_game')
                                .annotate(count_win=Count('pk', filter=Q(result=BetResultEnum.WIN)),
                                          count_drawn=Count('pk', filter=Q(result=BetResultEnum.DRAWN)),
                                          count_lose=Count('pk', filter=Q(result=BetResultEnum.LOSE)),)
                                .order_by('date_game'))
        qs_last_line = self._cumulative_result_counts(qs_last_line_raw)

        qs_last_bar_raw = (self.get_queryset()
                               .filter(date_game__range=[now().date() - relativedelta(days=30), now().date()])
                               .values('date_game')
                               .annotate(count_win=Count('pk', filter=Q(result=BetResultEnum.WIN)),
                                         count_drawn=Count('pk', filter=Q(result=BetResultEnum.DRAWN)),
                                         count_lose=Count('pk', filter=Q(result=BetResultEnum.LOSE)), )
                               .order_by('date_game'))
        qs_last_bar = self._structure_bars(qs_last_bar_raw)

        qs_months_line_raw = (self.get_queryset()
                                  .filter(date_game__lte=now().date())
                                  .annotate(date=TruncMonth('date_game'))
                                  .values('date')
                                  .annotate(count_win=Count('pk', filter=Q(result=BetResultEnum.WIN)),
                                            count_drawn=Count('pk', filter=Q(result=BetResultEnum.DRAWN)),
                                            count_lose=Count('pk', filter=Q(result=BetResultEnum.LOSE)),)
                                  .order_by('date'))
        qs_months_line = self._cumulative_result_counts(qs_months_line_raw, date_field='date')

        qs_months_bar_raw = (self.get_queryset()
                                 .filter(date_game__lte=now().date())
                                 .annotate(date=TruncMonth('date_game'))
                                 .values('date')
                                 .annotate(count_win=Count('pk', filter=Q(result=BetResultEnum.WIN)),
                                           count_drawn=Count('pk', filter=Q(result=BetResultEnum.DRAWN)),
                                           count_lose=Count('pk', filter=Q(result=BetResultEnum.LOSE)), )
                                 .order_by('date'))
        qs_months_bar = self._structure_bars(qs_months_bar_raw, date_field='date')

        qs_years_line_raw = (self.get_queryset()
                                 .filter(date_game__lte=now().date())
                                 .annotate(date=TruncYear('date_game'))
                                 .values('date')
                                 .annotate(count_win=Count('pk', filter=Q(result=BetResultEnum.WIN)),
                                           count_drawn=Count('pk', filter=Q(result=BetResultEnum.DRAWN)),
                                           count_lose=Count('pk', filter=Q(result=BetResultEnum.LOSE)),)
                                 .order_by('date'))
        qs_years_line = self._cumulative_result_counts(qs_years_line_raw, date_field='date')

        qs_years_bar_raw = (self.get_queryset()
                                .filter(date_game__lte=now().date())
                                .annotate(date=TruncYear('date_game'))
                                .values('date')
                                .annotate(count_win=Count('pk', filter=Q(result=BetResultEnum.WIN)),
                                          count_drawn=Count('pk', filter=Q(result=BetResultEnum.DRAWN)),
                                          count_lose=Count('pk', filter=Q(result=BetResultEnum.LOSE)), )
                                .order_by('date'))
        qs_years_bar = self._structure_bars(qs_years_bar_raw, date_field='date')

        qs = self.model.objects.none()    # імітація пустого queryset

        if chart_type == ChartType.LINE:
            if date_type == ChartDateType.NOW:
                qs = qs_now_line
            elif date_type == ChartDateType.LAST_30_DAYS:
                qs = qs_last_line
            elif date_type == ChartDateType.MONTHS:
                qs = qs_months_line
            elif date_type == ChartDateType.YEARS:
                qs = qs_years_line
        elif chart_type == ChartType.BAR:
            if date_type == ChartDateType.NOW:
                qs = qs_now_bar
            elif date_type == ChartDateType.LAST_30_DAYS:
                qs = qs_last_bar
            elif date_type == ChartDateType.MONTHS:
                qs = qs_months_bar
            elif date_type == ChartDateType.YEARS:
                qs = qs_years_bar

        return qs

    def _get_chart_data(self, chart_type=ChartType.LINE, date_type=ChartDateType.NOW, date_format='%Y-%m-%d'):
        data = {}
        qs = self._get_chart_queryset(chart_type, date_type)

        graph_start_date = None
        if date_type == ChartDateType.NOW:
            graph_start_date = now().date().replace(day=1)
        elif date_type == ChartDateType.LAST_30_DAYS:
            graph_start_date = now().date() - relativedelta(days=30)

        for elem in qs:

            day_date = elem.get('date_game') or elem.get('date')
            if graph_start_date and day_date < graph_start_date:
                continue
            date_str = day_date.strftime(date_format)

            if not data.get(date_str):
                data.update({date_str: {BetResultEnum.WIN: 0, BetResultEnum.DRAWN: 0, BetResultEnum.LOSE: 0}})
            data[date_str].update({elem.get('result'): elem.get('count')})

        return data

    def base_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetProfitGraphFilterForm(self.request.GET)
        filter_form.fields['sport_kind'].choices = SportKind.name_choices()
        filter_form.fields['betting_service'].choices = BettingService.name_choices()

        context.update({
            'profit_last_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.MONTHS, date_format='%Y-%m')),
            'profit_year_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.YEARS, date_format='%Y')),

            'profit_line_ykeys': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN, BetResultEnum.LOSE]),
            'profit_line_labels': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN, BetResultEnum.LOSE]),

            'profit_last_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.LAST_30_DAYS)),
            'profit_month_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.MONTHS, date_format='%Y-%m')),
            'profit_year_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.YEARS, date_format='%Y')),

            'profit_bar_ykeys': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN, BetResultEnum.LOSE]),
            'profit_bar_labels': json.dumps([BetResultEnum.WIN, BetResultEnum.DRAWN, BetResultEnum.LOSE]),

            'filter_form': filter_form,
            'title': 'Результати',
            'menu_key': 'bet_graphs_result',
        })
        return context


class BetGraphsRoiView(BetFilterMixin, ListView):
    model = BetBase
    template_name = 'bet/bet_graphs_roi.html'

    def _get_chart_queryset(self, chart_type=ChartType.LINE, date_type=ChartDateType.NOW):
        qs_now_line = (self.get_queryset()
                           .filter(date_game__lte=now().date())
                           .distinct('date_game')
                           .annotate(profit_sum=Window(
                                         expression=Sum("profit"),
                                         partition_by=None,
                                         order_by="date_game"),
                                     amount_sum=Window(
                                         expression=Sum("amount"),
                                         partition_by=None,
                                         order_by="date_game"),
                                     count=Window(
                                         expression=Count("pk"),
                                         partition_by=None,
                                         order_by="date_game"))
                           .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
                           .values('date_game', 'roi', 'count')
                           .order_by('date_game'))

        qs_now_bar = (self.get_queryset()
                          .distinct('date_game')
                          .filter(date_game__range=[now().date().replace(day=1), now().date()])
                          .annotate(profit_sum=Window(
                                        expression=Sum("profit"),
                                        partition_by=F("date_game"),
                                        order_by="date_game"),
                                    amount_sum=Window(
                                        expression=Sum("amount"),
                                        partition_by=F("date_game"),
                                        order_by="date_game"),
                                    count=Window(
                                        expression=Count("pk"),
                                        partition_by=F("date_game"),
                                        order_by="date_game"))
                          .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
                          .values('date_game', 'roi', 'count')
                          .order_by('date_game'))

        qs_last_line = (self.get_queryset()
                            .filter(date_game__lte=now().date())
                            .distinct('date_game')
                            .annotate(profit_sum=Window(
                                          expression=Sum("profit"),
                                          partition_by=None,
                                          order_by="date_game"),
                                      amount_sum=Window(
                                          expression=Sum("amount"),
                                          partition_by=None,
                                          order_by="date_game"),
                                      count=Window(
                                          expression=Count("pk"),
                                          partition_by=None,
                                          order_by="date_game"))
                            .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
                            .values('date_game', 'roi', 'count')
                            .order_by('date_game'))

        qs_last_bar = (self.get_queryset()
                           .distinct('date_game')
                           .filter(date_game__range=[now().date() - relativedelta(days=30), now().date()])
                           .annotate(profit_sum=Window(
                                         expression=Sum("profit"),
                                         partition_by=F("date_game"),
                                         order_by="date_game"),
                                     amount_sum=Window(
                                         expression=Sum("amount"),
                                         partition_by=F("date_game"),
                                         order_by="date_game"),
                                     count=Window(
                                         expression=Count("pk"),
                                         partition_by=F("date_game"),
                                         order_by="date_game"))
                           .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
                           .values('date_game', 'roi', 'count')
                           .order_by('date_game'))

        qs_months_line = (self.get_queryset()
                              .filter(date_game__lte=now().date())
                              .annotate(month=TruncMonth('date_game'))
                              .distinct('date_game')
                              .annotate(profit_sum=Window(
                                            expression=Sum("profit"),
                                            partition_by=None,
                                            order_by="month"),
                                        amount_sum=Window(
                                            expression=Sum("amount"),
                                            partition_by=None,
                                            order_by="month"),
                                        count=Window(
                                            expression=Count("pk"),
                                            partition_by=None,
                                            order_by="month"))
                              .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
                              .values('date_game', 'roi', 'count')
                              .order_by('date_game'))

        qs_months_bar = (self.get_queryset()
                             .filter(date_game__lte=now().date())
                             .annotate(month=TruncMonth('date_game'))
                             .distinct('date_game')
                             .annotate(profit_sum=Window(
                                           expression=Sum("profit"),
                                           partition_by="month",
                                           order_by="month"),
                                       amount_sum=Window(
                                           expression=Sum("amount"),
                                           partition_by="month",
                                           order_by="month"),
                                       count=Window(
                                           expression=Count("pk"),
                                           partition_by="month",
                                           order_by="month"))
                             .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
                             .values('date_game', 'roi', 'count')
                             .order_by('date_game'))

        qs_years_line = (self.get_queryset()
                             .filter(date_game__lte=now().date())
                             .annotate(year=TruncYear('date_game'))
                             .distinct('date_game')
                             .annotate(profit_sum=Window(
                                           expression=Sum("profit"),
                                           partition_by=None,
                                           order_by="year"),
                                       amount_sum=Window(
                                           expression=Sum("amount"),
                                           partition_by=None,
                                           order_by="year"),
                                       count=Window(
                                           expression=Count("pk"),
                                           partition_by=None,
                                           order_by="year"))
                             .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
                             .values('date_game', 'roi', 'count')
                             .order_by('date_game'))

        qs_years_bar = (self.get_queryset()
                            .filter(date_game__lte=now().date())
                            .annotate(year=TruncYear('date_game'))
                            .distinct('date_game')
                            .annotate(profit_sum=Window(
                                          expression=Sum("profit"),
                                          partition_by='year',
                                          order_by="year"),
                                      amount_sum=Window(
                                          expression=Sum("amount"),
                                          partition_by='year',
                                          order_by="year"),
                                      count=Window(
                                          expression=Count("pk"),
                                          partition_by='year',
                                          order_by="year"))
                            .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
                            .values('date_game', 'roi', 'count')
                            .order_by('date_game'))

        qs = self.model.objects.none()  # імітація пустого queryset

        if chart_type == ChartType.LINE:
            if date_type == ChartDateType.NOW:
                qs = qs_now_line
            elif date_type == ChartDateType.LAST_30_DAYS:
                qs = qs_last_line
            elif date_type == ChartDateType.MONTHS:
                qs = qs_months_line
            elif date_type == ChartDateType.YEARS:
                qs = qs_years_line
        elif chart_type == ChartType.BAR:
            if date_type == ChartDateType.NOW:
                qs = qs_now_bar
            elif date_type == ChartDateType.LAST_30_DAYS:
                qs = qs_last_bar
            elif date_type == ChartDateType.MONTHS:
                qs = qs_months_bar
            elif date_type == ChartDateType.YEARS:
                qs = qs_years_bar

        return qs

    def _get_chart_data(self, chart_type=ChartType.LINE, date_type=ChartDateType.NOW, date_format='%Y-%m-%d'):
        data = {}
        qs = self._get_chart_queryset(chart_type, date_type)

        graph_start_date = None
        if date_type == ChartDateType.NOW:
            graph_start_date = now().date().replace(day=1)
        elif date_type == ChartDateType.LAST_30_DAYS:
            graph_start_date = now().date() - relativedelta(days=30)

        for elem in qs:
            day_date = elem.get('date_game')
            if graph_start_date and day_date < graph_start_date:
                continue
            date_str = day_date.strftime(date_format)
            roi = elem.get('roi', 0.00)
            count = elem.get('count', 0)
            data.update({date_str: {'Рентабельність (%)': round(float(roi), 2), 'count': count}})
        return data

    def base_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetProfitGraphFilterForm(self.request.GET)
        filter_form.fields['sport_kind'].choices = SportKind.name_choices()
        filter_form.fields['betting_service'].choices = BettingService.name_choices()

        context.update({
            'roi_last_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.LAST_30_DAYS)),
            'roi_month_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.MONTHS, date_format='%Y-%m')),
            'roi_year_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.YEARS, date_format='%Y')),
            'roi_line_ykeys': json.dumps(["Рентабельність (%)"]),
            'roi_line_labels': json.dumps(["Рентабельність (%)"]),

            'roi_last_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.LAST_30_DAYS)),
            'roi_month_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.MONTHS, date_format='%Y-%m')),
            'roi_year_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.YEARS, date_format='%Y')),
            'roi_bar_ykeys': json.dumps(["Рентабельність (%)"]),
            'roi_bar_labels': json.dumps(["Рентабельність (%)"]),

            'filter_form': filter_form,
            'title': 'Рентабельність',
            'menu_key': 'bet_graphs_roi',
        })
        return context


class BetCreateView(CreateView):
    form_class = BetCreateForm
    template_name = 'bet/bet_create.html'
    success_url = reverse_lazy('bet_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        bet_create_form = self.form_class()
        bet_create_form.fields['user'].initial = self.request.user.pk
        bet_create_form.fields['user'].widget = HiddenInput()
        bet_create_form.fields['sport_kind'].choices = SportKind.name_choices()
        bet_create_form.fields['betting_service'].choices = BettingService.name_choices()

        football_create_form = BetFootballCreateForm()
        football_create_form.fields['user'].initial = self.request.user.pk
        football_create_form.fields['user'].widget = HiddenInput()
        football_create_form.fields['competition'].choices = CompetitionBase.name_choices()
        football_create_form.fields['betting_service'].choices = BettingService.name_choices()

        context.update({
            'title': 'Додати ставку',
            'bet_create_form': bet_create_form,
            'football_create_form': football_create_form,
            'menu_key': 'bet_create',
        })

        return context


class BetBaseChangeFavouriteStatusView(DetailView):
    model = BetBase
    pk_url_kwarg = 'id'

    def get_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

    def get(self, request, *args, **kwargs):
        self.get_object().change_is_favourite()
        return redirect(reverse_lazy('bet_list') + f'?{self.request.GET.urlencode()}')


class BetBaseDeleteView(DetailView):
    model = BetBase
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect(reverse_lazy('bet_list') + f'?{self.request.GET.urlencode()}')


class BetFootballCreateView(CreateView):
    form_class = BetFootballCreateForm
    template_name = 'bet/bet_football_create.html'
    success_url = reverse_lazy('bet_football_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'].fields['user'].initial = self.request.user.pk
        context['form'].fields['user'].widget = HiddenInput()
        context.update({
            'menu_key': 'bet_football_create',
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        return redirect(reverse_lazy('bet_create'))


class BetFootballChangeFavouriteStatusView(DetailView):
    model = BetFootball
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().change_is_favourite()
        return redirect(reverse_lazy('bet_football_list') + f'?{self.request.GET.urlencode()}')


class BetFootballDeleteView(DetailView):
    model = BetFootball
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect(reverse_lazy('bet_football_list') + f'?{self.request.GET.urlencode()}')


class BetGraphsAvgAmountView(BetFilterMixin, ListView):
    model = BetBase
    template_name = 'bet/bet_graphs_amount.html'

    def _get_chart_queryset(self, chart_type=ChartType.LINE, date_type=ChartDateType.NOW):
        qs_now_line = (self.get_queryset()
                           .filter(date_game__lte=now().date())
                           .distinct('date_game')
                           .annotate(amount_avg=Window(
                                         expression=Avg("amount"),
                                         partition_by=None,
                                         order_by="date_game"),
                                     count=Window(
                                         expression=Count("pk"),
                                         partition_by=None,
                                         order_by="date_game"))
                           .values('date_game', 'amount_avg', 'count')
                           .order_by('date_game'))

        qs_now_bar = (self.get_queryset()
                          .distinct('date_game')
                          .filter(date_game__range=[now().date().replace(day=1), now().date()])
                          .annotate(amount_avg=Window(
                                        expression=Avg("amount"),
                                        partition_by=F("date_game"),
                                        order_by="date_game"),
                                    count=Window(
                                        expression=Count("pk"),
                                        partition_by=F("date_game"),
                                        order_by="date_game"))
                          .values('date_game', 'amount_avg', 'count')
                          .order_by('date_game'))

        qs_last_line = (self.get_queryset()
                            .filter(date_game__lte=now().date())
                            .distinct('date_game')
                            .annotate(amount_avg=Window(
                                          expression=Avg("amount"),
                                          partition_by=None,
                                          order_by="date_game"),
                                      count=Window(
                                          expression=Count("pk"),
                                          partition_by=None,
                                          order_by="date_game"))
                            .values('date_game', 'amount_avg', 'count')
                            .order_by('date_game'))

        qs_last_bar = (self.get_queryset()
                           .distinct('date_game')
                           .filter(date_game__range=[now().date() - relativedelta(days=30), now().date()])
                           .annotate(amount_avg=Window(
                                         expression=Avg("amount"),
                                         partition_by=F("date_game"),
                                         order_by="date_game"),
                                     count=Window(
                                         expression=Count("pk"),
                                         partition_by=F("date_game"),
                                         order_by="date_game"))
                           .values('date_game', 'amount_avg', 'count')
                           .order_by('date_game'))

        qs_months_line = (self.get_queryset()
                              .filter(date_game__lte=now().date())
                              .annotate(month=TruncMonth('date_game'))
                              .distinct('date_game')
                              .annotate(amount_avg=Window(
                                            expression=Avg("amount"),
                                            partition_by=None,
                                            order_by="month"),
                                        count=Window(
                                            expression=Count("pk"),
                                            partition_by=None,
                                            order_by="month"))
                              .values('date_game', 'amount_avg', 'count')
                              .order_by('date_game'))

        qs_months_bar = (self.get_queryset()
                             .filter(date_game__lte=now().date())
                             .annotate(month=TruncMonth('date_game'))
                             .distinct('date_game')
                             .annotate(amount_avg=Window(
                                           expression=Avg("amount"),
                                           partition_by="month",
                                           order_by="month"),
                                       count=Window(
                                           expression=Count("pk"),
                                           partition_by="month",
                                           order_by="month"))
                             .values('date_game', 'amount_avg', 'count')
                             .order_by('date_game'))

        qs_years_line = (self.get_queryset()
                             .filter(date_game__lte=now().date())
                             .annotate(year=TruncYear('date_game'))
                             .distinct('date_game')
                             .annotate(amount_avg=Window(
                                           expression=Avg("amount"),
                                           partition_by=None,
                                           order_by="year"),
                                       count=Window(
                                           expression=Count("pk"),
                                           partition_by=None,
                                           order_by="year"))
                             .values('date_game', 'amount_avg', 'count')
                             .order_by('date_game'))

        qs_years_bar = (self.get_queryset()
                            .filter(date_game__lte=now().date())
                            .annotate(year=TruncYear('date_game'))
                            .distinct('date_game')
                            .annotate(amount_avg=Window(
                                          expression=Avg("amount"),
                                          partition_by='year',
                                          order_by="year"),
                                      count=Window(
                                          expression=Count("pk"),
                                          partition_by='year',
                                          order_by="year"))
                            .values('date_game', 'amount_avg', 'count')
                            .order_by('date_game'))

        qs = self.model.objects.none()  # імітація пустого queryset

        if chart_type == ChartType.LINE:
            if date_type == ChartDateType.NOW:
                qs = qs_now_line
            elif date_type == ChartDateType.LAST_30_DAYS:
                qs = qs_last_line
            elif date_type == ChartDateType.MONTHS:
                qs = qs_months_line
            elif date_type == ChartDateType.YEARS:
                qs = qs_years_line
        elif chart_type == ChartType.BAR:
            if date_type == ChartDateType.NOW:
                qs = qs_now_bar
            elif date_type == ChartDateType.LAST_30_DAYS:
                qs = qs_last_bar
            elif date_type == ChartDateType.MONTHS:
                qs = qs_months_bar
            elif date_type == ChartDateType.YEARS:
                qs = qs_years_bar

        return qs

    def _get_chart_data(self, chart_type=ChartType.LINE, date_type=ChartDateType.NOW, date_format='%Y-%m-%d'):
        data = {}
        qs = self._get_chart_queryset(chart_type, date_type)

        graph_start_date = None
        if date_type == ChartDateType.NOW:
            graph_start_date = now().date().replace(day=1)
        elif date_type == ChartDateType.LAST_30_DAYS:
            graph_start_date = now().date() - relativedelta(days=30)

        for elem in qs:
            day_date = elem.get('date_game')
            if graph_start_date and day_date < graph_start_date:
                continue
            date_str = day_date.strftime(date_format)
            amount_avg = elem.get('amount_avg', 0.00)
            count = elem.get('count', 0)
            data.update({date_str: {'Середня ставка': round(float(amount_avg), 2), 'count': count}})
        return data

    def base_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        filter_form = BetProfitGraphFilterForm(self.request.GET)
        filter_form.fields['sport_kind'].choices = SportKind.name_choices()
        filter_form.fields['betting_service'].choices = BettingService.name_choices()

        context.update({
            'amount_last_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.LAST_30_DAYS)),
            'amount_month_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.MONTHS, date_format='%Y-%m')),
            'amount_year_line_data': MorrisChartLine.to_json_data(
                self._get_chart_data(chart_type=ChartType.LINE, date_type=ChartDateType.YEARS, date_format='%Y-%m')),
            'amount_line_ykeys': json.dumps(["Середня ставка"]),
            'amount_line_labels': json.dumps(["Середня ставка"]),

            'amount_last_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.LAST_30_DAYS)),
            'amount_month_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.MONTHS, date_format='%Y-%m')),
            'amount_year_bar_data': MorrisChartBar.to_json_data(
                self._get_chart_data(chart_type=ChartType.BAR, date_type=ChartDateType.YEARS, date_format='%Y-%m')),
            'amount_bar_ykeys': json.dumps(["Середня ставка"]),
            'amount_bar_labels': json.dumps(["Середня ставка"]),

            'filter_form': filter_form,
            'title': 'Середня ставка',
            'menu_key': 'bet_graphs_amount',
        })
        return context


class RatingsView(BetFilterMixin, ListView):
    model = BetBase
    template_name = 'bet/rating.html'

    def get_active_tab(self):
        return int(self.request.GET.get('active_tab', 1))

    def annotate_qs(self, queryset, field_name, fields_dict):
        ordering_tab = '-profit_sum'
        ordering_tab_raw_value = self.request.GET.get('ordering_tab')
        desc = True if self.request.GET.get('ordering_type') == 'Desc' else False

        if ordering_tab_raw_value:
            ordering_tab_value = reverse_dict(fields_dict).get(ordering_tab_raw_value)
            if ordering_tab_value:
                if desc:
                    ordering_tab = ordering_tab_value
                else:
                    ordering_tab = f"-{ordering_tab_value}"

        qs = (queryset
              .values(field_name)
              .annotate(profit_avg=Avg('profit'), profit_sum=Sum('profit'), amount_sum=Sum('amount'), count=Count('pk'))
              .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
              .annotate(count_win=Count(Case(When(result=BetResultEnum.WIN, then=1),
                                             output_field=IntegerField())))
              .annotate(count_drawn=Count(Case(When(result=BetResultEnum.DRAWN, then=1),
                                               output_field=IntegerField())))
              .annotate(count_lose=Count(Case(When(result=BetResultEnum.LOSE, then=1),
                                              output_field=IntegerField())))
              .order_by(ordering_tab))
        print(qs)
        return qs

    def get_sport_kind_data(self):
        data = []

        for obj in self.annotate_qs(self.get_queryset(), 'sport_kind__name', SPORT_KIND_RATING_TABLE_FIELD_NAMES):
            data.append({
                'name': obj.get('sport_kind__name') or 'Iнше',
                'avg_profit': round(float(obj.get('profit_avg', 0.00)), 2),
                'total_profit': round(float(obj.get('profit_sum', 0.00)), 2),
                'total_roi': round(float(obj.get('roi', 0.00)), 2),
                'count': obj.get('count', 0),

                'count_win': obj.get('count_win', 0),
                'count_drawn': obj.get('count_drawn', 0),
                'count_lose': obj.get('count_lose', 0),
            })
            print(data)
        return data

    def base_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        filter_form = RatingFilterForm(self.request.GET)
        filter_form.fields['betting_service'].choices = BettingService.name_choices()

        context.update({
            'title': 'Рейтинги',
            'menu_key': 'bet_ratings',
            'filter_form': filter_form,
            'active_tab': self.get_active_tab(),
            'sport_kind_objects': self.get_sport_kind_data(),
            'sport_kind_fields': SPORT_KIND_RATING_TABLE_FIELD_NAMES.values(),
        })

        return context


class RatingFootballView(BetFilterMixin, ListView):
    model = BetFootball
    template_name = 'bet/rating_football.html'

    def get_active_tab(self):
        return int(self.request.GET.get('active_tab', 1))

    def annotate_qs(self, queryset, field_name, fields_dict):
        ordering_tab = '-profit_sum'
        ordering_tab_raw_value = self.request.GET.get('ordering_tab')
        desc = True if self.request.GET.get('ordering_type') == 'Desc' else False

        if ordering_tab_raw_value:
            ordering_tab_value = reverse_dict(fields_dict).get(ordering_tab_raw_value)
            if ordering_tab_value:
                if desc:
                    ordering_tab = ordering_tab_value
                else:
                    ordering_tab = f"-{ordering_tab_value}"

        qs = (queryset
              .values(field_name)
              .annotate(profit_avg=Avg('profit'), profit_sum=Sum('profit'), amount_sum=Sum('amount'), count=Count('pk'))
              .annotate(roi=F('profit_sum') * 100 / F('amount_sum'))
              .annotate(count_win=Count(Case(When(result=BetResultEnum.WIN, then=1),
                        output_field=IntegerField())))
              .annotate(count_drawn=Count(Case(When(result=BetResultEnum.DRAWN, then=1),
                        output_field=IntegerField())))
              .annotate(count_lose=Count(Case(When(result=BetResultEnum.LOSE, then=1),
                        output_field=IntegerField())))
              .order_by(ordering_tab))
        return qs

    def get_competitions_data(self):
        data = []
        for obj in self.annotate_qs(self.get_queryset(), 'competition__name', COMPETITION_RATING_TABLE_FIELD_NAMES):
            try:
                flag = CompetitionBase.objects.get(name=obj.get('competition__name')).country.flag_code
            except:
                flag = ''
            data.append({
                'flag': flag,
                'name': obj.get('competition__name') or 'Iнше',
                'avg_profit': round(float(obj.get('profit_avg', 0.00)), 2),
                'total_profit': round(float(obj.get('profit_sum', 0.00)), 2),
                'total_roi': round(float(obj.get('roi', 0.00)), 2),
                'count': obj.get('count', 0),

                'count_win': obj.get('count_win', 0),
                'count_drawn': obj.get('count_drawn', 0),
                'count_lose': obj.get('count_lose', 0),

            })
        return data

    def get_bet_type_data(self):
        data = []
        for obj in self.annotate_qs(self.get_queryset(), 'bet_type', BET_TYPE_RATING_TABLE_FIELD_NAMES):
            data.append({
                'name': obj.get('bet_type') or BetFootballTypeEnum.UNKNOWN,
                'avg_profit': round(float(obj.get('profit_avg', 0.00)), 2),
                'total_profit': round(float(obj.get('profit_sum', 0.00)), 2),
                'total_roi': round(float(obj.get('roi', 0.00)), 2),
                'count': obj.get('count', 0),

                'count_win': obj.get('count_win', 0),
                'count_drawn': obj.get('count_drawn', 0),
                'count_lose': obj.get('count_lose', 0),
            })
        return data

    def base_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

    def get_queryset(self):
        filtered_qs = self.filtered_queryset(self.base_queryset())
        return filtered_qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        filter_form = RatingFilterForm(self.request.GET)
        filter_form.fields['betting_service'].choices = BettingService.name_choices()

        context.update({
            'title': 'Рейтинги Футбол',
            'menu_key': 'bet_ratings_football',
            'filter_form': filter_form,
            'active_tab': self.get_active_tab(),
            'competition_objects': self.get_competitions_data(),
            'competition_fields': COMPETITION_RATING_TABLE_FIELD_NAMES.values(),
            'bet_type_objects': self.get_bet_type_data(),
            'bet_type_fields': BET_TYPE_RATING_TABLE_FIELD_NAMES.values(),
        })

        return context


class CalendarView(ListView):
    model = BetBase
    template_name = 'bet/calendar.html'

    def get_queryset(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.none()

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
            'title': 'Календар',
            'menu_key': 'bet_calendar',
            'calendar_data': CalendarDashboard.to_json_data(self._prepare_calendar_data()),
            'date_now': json.dumps(datetime.strftime(now().date(), '%Y-%m-%d'))
        })
        return context


class ProfileView(BetFilterMixin, ListView):
    model = BetBase
    template_name = 'bet/profile.html'

    def get_active_tab(self):
        return int(self.request.GET.get('active_tab', 1))

    def ordered_qs(self, qs):
        print(qs)
        ordering = self.request.GET.get('ordering')
        print(ordering)
        if ordering:
            try:
                qs = qs.order_by(ordering, '-id')
            except Exception as e:
                print(e)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        sport_kind_objects = self.ordered_qs(self.request.user.sport_kinds.all())
        competition_objects = self.ordered_qs(self.request.user.competitions.all())
        service_objects = self.ordered_qs(self.request.user.services.filter())

        create_sport_kind_form = SportKindCreateForm()
        create_sport_kind_form.fields['user'].initial = self.request.user.pk
        create_sport_kind_form.fields['user'].widget = HiddenInput()

        create_service_form = ServiceCreateForm()
        create_service_form.fields['user'].initial = self.request.user.pk
        create_service_form.fields['user'].widget = HiddenInput()

        create_competition_form = CompetitionCreateForm()
        create_competition_form.fields['user'].initial = self.request.user.pk
        create_competition_form.fields['user'].widget = HiddenInput()
        create_competition_form.fields['sport_kind'].choices = SportKind.name_choices()

        context.update({
            'title': 'Профіль',
            'menu_key': 'bet_profile',

            'sport_kind_objects': sport_kind_objects,
            'competition_objects': competition_objects,
            'service_objects': service_objects,

            'sport_kind_table_fields': ['Назва'],
            'competition_table_fields': ['Країна', 'Назва', 'Вид спорту'],
            'service_table_fields': ['Назва'],

            'create_sport_kind_form': create_sport_kind_form,
            'create_competition_form': create_competition_form,
            'create_service_form': create_service_form,

            'active_tab': self.get_active_tab(),
        })
        print(context['active_tab'])
        return context


class SportKindCreateView(CreateView):
    form_class = SportKindCreateForm
    success_url = reverse_lazy('bet_profile')


class CompetitionCreateView(CreateView):
    form_class = CompetitionCreateForm
    success_url = reverse_lazy('bet_profile')


class ServiceCreateView(CreateView):
    form_class = ServiceCreateForm
    success_url = reverse_lazy('bet_profile')


class SportKindDeleteView(DetailView):
    model = SportKind
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect(reverse_lazy('bet_profile') + f'?{self.request.GET.urlencode()}')


class CompetitionDeleteView(DetailView):
    model = CompetitionBase
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect(reverse_lazy('bet_profile') + f'?{self.request.GET.urlencode()}')


class BettingServiceDeleteView(DetailView):
    model = BettingService
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect(reverse_lazy('bet_profile') + f'?{self.request.GET.urlencode()}')
