from datetime import datetime
from django.db.models import Q


class BetFilterMixin:

    def filtered_queryset(self, qs):
        search_value = self.request.GET.get('search')
        if search_value:
            qs = qs.filter(
                Q(team_home__name__icontains=search_value) | Q(team_guest__name__icontains=search_value)
            )

        sport_kind_values = self.request.GET.getlist('sport_kind')
        if sport_kind_values:
            qs = qs.filter(sport_kind__name__in=sport_kind_values)

        betting_service_values = self.request.GET.getlist('betting_service')
        if betting_service_values:
            qs = qs.filter(betting_service__name__in=betting_service_values)

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

        live_types = self.request.GET.getlist('live_type')
        if live_types:
            qs = qs.filter(live_type__in=live_types)

        bet_type = self.request.GET.getlist('bet_type')
        if bet_type:
            qs = qs.filter(bet_type__in=bet_type)

        is_favourite_value = self.request.GET.getlist('is_favourite')
        if is_favourite_value:
            qs = qs.filter(is_favourite__in=is_favourite_value)

        ordering = self.request.GET.get('ordering')
        if ordering:
            if ordering == 'is_favourite':
                qs = qs.order_by('-is_favourite', '-id')
            else:
                qs = qs.order_by(ordering, '-id')

        coefficient_min = self.request.GET.get('coefficient_min')
        if coefficient_min:
            qs = qs.filter(coefficient__gte=coefficient_min)

        coefficient_max = self.request.GET.get('coefficient_max')
        if coefficient_max:
            qs = qs.filter(coefficient__lte=coefficient_max)

        game_status = self.request.GET.getlist('game_status')
        if game_status:
            qs = qs.filter(game_status__in=game_status)

        competition_values = self.request.GET.getlist('competition')
        if competition_values:
            qs = qs.filter(competition__name__in=competition_values)

        return qs
