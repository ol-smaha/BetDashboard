from django.urls import path


from bet.views import (BetHistoryView, BetGraphsView, Statistic, BetGraphsProfitView, BetGraphsResultView,
                       FootballBetHistoryView, BetGraphsRoiView, BetCreateView, BetBaseChangeFavouriteStatusView,
                       BetBaseDeleteView, BetFootballChangeFavouriteStatusView, BetFootballDeleteView,
                       BetFootballCreateView, BetGraphsAvgAmountView, RatingGraphsView, CalendarView)

urlpatterns = [
    path('list/', BetHistoryView.as_view(), name='bet_list'),
    path('create/', BetCreateView.as_view(), name='bet_create'),
    path('delete/<int:id>', BetBaseDeleteView.as_view(), name='bet_delete'),
    path('change-is-favourite/<int:id>', BetBaseChangeFavouriteStatusView.as_view(),
         name='bet_change_is_favourite'),

    path('list/football/', FootballBetHistoryView.as_view(), name='bet_football_list'),
    path('create/football/', BetFootballCreateView.as_view(), name='bet_football_create'),
    path('delete/football/<int:id>', BetFootballDeleteView.as_view(), name='bet_football_delete'),
    path('change-is-favourite/football/<int:id>', BetFootballChangeFavouriteStatusView.as_view(),
         name='bet_football_change_is_favourite'),

    # path('graphs/', BetGraphsView.as_view(), name='bet_graphs'),
    path('graphs/profit/', BetGraphsProfitView.as_view(), name='bet_graphs_profit'),
    path('graphs/roi/', BetGraphsRoiView.as_view(), name='bet_graphs_roi'),
    path('graphs/result/', BetGraphsResultView.as_view(), name='bet_graphs_result'),
    path('graphs/amount/', BetGraphsAvgAmountView.as_view(), name='bet_graphs_amount'),

    path('calendar/', CalendarView.as_view(), name='bet_calendar'),
    path('statistic/', Statistic.as_view(), name='bet_statistic'),
    path('ratings/', RatingGraphsView.as_view(), name='bet_ratings'),
]
