from django.urls import path


from bet.views import (BetHistoryView, BetGraphsView, Statistic, BetGraphsProfitView, BetGraphsResultView,
                       FootballBetHistoryView, BetGraphsRoiView, BetCreateView, BetBaseChangeFavouriteStatusView,
                       BetBaseDeleteView, BetFootballChangeFavouriteStatusView, BetFootballDeleteView,
                       BetFootballCreateView)

urlpatterns = [
    path('history/', BetHistoryView.as_view(), name='bet_history'),
    path('create/', BetCreateView.as_view(), name='bet_create'),
    path('delete/<int:id>', BetBaseDeleteView.as_view(), name='bet_delete'),
    path('change_favourite_status/<int:id>', BetBaseChangeFavouriteStatusView.as_view(), name='bet_change_favourite_status'),
    path('graphs/', BetGraphsView.as_view(), name='bet_graphs'),
    path('graphs/profit/', BetGraphsProfitView.as_view(), name='bet_graphs_profit'),
    path('graphs/result/', BetGraphsResultView.as_view(), name='bet_graphs_result'),
    path('statistic/', Statistic.as_view(), name='statistic'),
    path('football_history/', FootballBetHistoryView.as_view(), name='football_history'),
    path('graphs/roi/', BetGraphsRoiView.as_view(), name='bet_graphs_roi'),
    path('create_football/', BetFootballCreateView.as_view(), name='bet_football_create'),
    path('delete_football/<int:id>', BetFootballDeleteView.as_view(), name='football_bet_delete'),
    path('change_favourite_status_football/<int:id>', BetFootballChangeFavouriteStatusView.as_view(), name='football_bet_change_favourite_status'),

]
