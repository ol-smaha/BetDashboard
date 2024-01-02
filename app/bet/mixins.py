from datetime import datetime
from django.db.models import Q, F


class BetFilterMixin:

    def filtered_queryset(self, qs):
        search_value = self.request.GET.get('search')
        if search_value:
            qs = qs.filter(
                Q(team_home__name__icontains=search_value) | Q(team_guest__name__icontains=search_value)
            )

        sport_kind_values = self.request.GET.getlist('sport_kind')
        if sport_kind_values:
            qs = qs.filter(sport_kind__id__in=sport_kind_values)

        betting_service_values = self.request.GET.getlist('betting_service')
        if betting_service_values:
            qs = qs.filter(betting_service__id__in=betting_service_values)

        date_game_start = self.request.GET.get('date_game_start')
        if date_game_start:
            qs = qs.filter(date_game__gte=datetime.strptime(date_game_start, '%d/%m/%Y'))

        date_game_end = self.request.GET.get('date_game_end')
        if date_game_end:
            qs = qs.filter(date_game__lte=datetime.strptime(date_game_end, '%d/%m/%Y'))

        amount_min = self.request.GET.get('amount_min')
        if amount_min:
            qs = qs.filter(amount__gte=amount_min)

        amount_max = self.request.GET.get('amount_max')
        if amount_max:
            qs = qs.filter(amount__lte=amount_max)

        result_value = self.request.GET.getlist('result')
        if result_value:
            qs = qs.filter(result__in=result_value)

        is_live_types = self.request.GET.getlist('is_live_type')
        if is_live_types:
            qs = qs.filter(is_live_type__in=is_live_types)

        bet_type = self.request.GET.getlist('bet_type')
        if bet_type:
            qs = qs.filter(bet_type__in=bet_type)

        is_favourite_value = self.request.GET.getlist('is_favourite')
        if is_favourite_value:
            qs = qs.filter(is_favourite__in=is_favourite_value)

        ordering = self.request.GET.get('ordering')
        desc = True if self.request.GET.get('ordering_type') == 'Desc' else False
        if ordering:
            if 'is_favourite' in ordering:
                if desc:
                    qs = qs.order_by('is_favourite', '-id')
                else:
                    qs = qs.order_by('-is_favourite', '-id')
            else:
                if desc:
                    qs = qs.order_by(F(ordering).desc(nulls_last=True), '-id')
                else:
                    qs = qs.order_by(F(ordering).asc(nulls_last=True), '-id')

        coefficient_min = self.request.GET.get('coefficient_min')
        if coefficient_min:
            qs = qs.filter(coefficient__gte=coefficient_min)

        coefficient_max = self.request.GET.get('coefficient_max')
        if coefficient_max:
            qs = qs.filter(coefficient__lte=coefficient_max)

        competition_values = self.request.GET.getlist('competition')
        if competition_values:
            qs = qs.filter(competition__id__in=competition_values)

        return qs
