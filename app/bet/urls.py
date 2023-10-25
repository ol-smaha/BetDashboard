from django.urls import path


from bet.views import BetHistoryView, BetGraphsView, Statistic

urlpatterns = [
    path('history/', BetHistoryView.as_view(), name='bet_history'),
    path('graphs/', BetGraphsView.as_view(), name='bet_graphs'),
    path('statistic/', Statistic.as_view(), name='statistic'),
]
