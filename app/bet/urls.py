from django.urls import path

from bet.views import BetHistoryView, BetGraphsView

urlpatterns = [
    path('history/', BetHistoryView.as_view(), name='bet_history'),
    path('graphs/', BetGraphsView.as_view(), name='bet_graphs'),
]
