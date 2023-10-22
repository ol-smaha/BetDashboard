from django.views.generic.list import ListView

from .constants import BET_BASE_TABLE_FIELD_NAMES
from .models import BetBase


class BetHistory(ListView):
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


class Graphs(ListView):
    model = BetBase
    template_name = 'bet/bet_graphs.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context_data = {
            'bets': self.get_queryset(),
            'title': 'Bets Graphs'
        }
        return context_data
