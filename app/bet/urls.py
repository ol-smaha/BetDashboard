from django.urls import path


from bet.views import (BetHistoryView, Statistic, BetGraphsProfitView, BetGraphsResultView,
                       FootballBetHistoryView, BetGraphsRoiView, BetCreateView, BetBaseChangeFavouriteStatusView,
                       BetBaseDeleteView, BetFootballChangeFavouriteStatusView, BetFootballDeleteView,
                       BetFootballCreateView, BetGraphsAvgAmountView, RatingGraphsView, CalendarView, ProfileView,
                       CompetitionCreateView, ServiceCreateView, SportKindCreateView, SportKindDeleteView,
                       BettingServiceDeleteView, CompetitionDeleteView)


urlpatterns = [
    path('list/', BetHistoryView.as_view(), name='bet_list'),
    path('create/', BetCreateView.as_view(), name='bet_create'),   # use modal form on bet_list
    path('delete/<int:id>', BetBaseDeleteView.as_view(), name='bet_delete'),
    path('change-is-favourite/<int:id>', BetBaseChangeFavouriteStatusView.as_view(),
         name='bet_change_is_favourite'),

    path('list/football/', FootballBetHistoryView.as_view(), name='bet_football_list'),
    path('create/football/', BetFootballCreateView.as_view(), name='bet_football_create'),   # use modal form on bet_football_list
    path('delete/football/<int:id>', BetFootballDeleteView.as_view(), name='bet_football_delete'),
    path('change-is-favourite/football/<int:id>', BetFootballChangeFavouriteStatusView.as_view(),
         name='bet_football_change_is_favourite'),

    path('graphs/profit/', BetGraphsProfitView.as_view(), name='bet_graphs_profit'),
    path('graphs/roi/', BetGraphsRoiView.as_view(), name='bet_graphs_roi'),
    path('graphs/result/', BetGraphsResultView.as_view(), name='bet_graphs_result'),
    path('graphs/amount/', BetGraphsAvgAmountView.as_view(), name='bet_graphs_amount'),

    path('calendar/', CalendarView.as_view(), name='bet_calendar'),
    path('statistic/', Statistic.as_view(), name='bet_statistic'),
    path('ratings/', RatingGraphsView.as_view(), name='bet_ratings'),

    path('profile/', ProfileView.as_view(), name='bet_profile'),

    path('sport_kind/create', SportKindCreateView.as_view(), name='create_sport_kind_form'),   # use modal form on bet_profile
    path('competition/create', CompetitionCreateView.as_view(), name='create_competition_form'),   # use modal form on bet_profile
    path('service/create', ServiceCreateView.as_view(), name='create_service_form'),   # use modal form on bet_profile

    path('sport_kind/delete/<int:id>', SportKindDeleteView.as_view(), name='bet_sport_kind_delete'),
    path('competition/delete/<int:id>', CompetitionDeleteView.as_view(), name='bet_competition_delete'),
    path('service/delete/<int:id>', BettingServiceDeleteView.as_view(), name='bet_service_delete'),

]
