from django.urls import path


from bet.views import BetHistoryView, BetGraphsView, Statistic, BetGraphsProfitView

urlpatterns = [
    path('history/', BetHistoryView.as_view(), name='bet_history'),
    path('graphs/', BetGraphsView.as_view(), name='bet_graphs'),
    path('graphs/profit/', BetGraphsProfitView.as_view(), name='bet_graphs_profit'),
    path('statistic/', Statistic.as_view(), name='statistic'),

]
