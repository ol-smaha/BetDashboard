from django.urls import path
from django.contrib.auth.decorators import login_required


from bet.views import (BetHistoryView, Statistic, BetGraphsProfitView, BetGraphsResultView,
                       FootballBetHistoryView, BetGraphsRoiView, BetCreateView, BetBaseChangeFavouriteStatusView,
                       BetBaseDeleteView, BetFootballChangeFavouriteStatusView, BetFootballDeleteView,
                       BetFootballCreateView, BetGraphsAvgAmountView, RatingsView, RatingFootballView, CalendarView,
                       ProfileView, CompetitionCreateView, ServiceCreateView, SportKindCreateView, SportKindDeleteView,
                       BettingServiceDeleteView, CompetitionDeleteView)


urlpatterns = [
    path('list/', login_required(BetHistoryView.as_view()), name='bet_list'),
    path('create/', login_required(BetCreateView.as_view()), name='bet_create'),   # use modal form on bet_list
    path('delete/<int:id>/', login_required(BetBaseDeleteView.as_view()), name='bet_delete'),
    path('change-is-favourite/<int:id>/', login_required(BetBaseChangeFavouriteStatusView.as_view()),
         name='bet_change_is_favourite'),

    path('list/football/', login_required(FootballBetHistoryView.as_view()), name='bet_football_list'),
    path('create/football/', login_required(BetFootballCreateView.as_view()), name='bet_football_create'),   # use modal form on bet_football_list
    path('delete/football/<int:id>/', login_required(BetFootballDeleteView.as_view()), name='bet_football_delete'),
    path('change-is-favourite/football/<int:id>/', login_required(BetFootballChangeFavouriteStatusView.as_view()),
         name='bet_football_change_is_favourite'),


    path('graphs/profit/', login_required(BetGraphsProfitView.as_view()), name='bet_graphs_profit'),
    path('graphs/roi/', login_required(BetGraphsRoiView.as_view()), name='bet_graphs_roi'),
    path('graphs/result/', login_required(BetGraphsResultView.as_view()), name='bet_graphs_result'),
    path('graphs/amount/', login_required(BetGraphsAvgAmountView.as_view()), name='bet_graphs_amount'),

    path('calendar/', login_required(CalendarView.as_view()), name='bet_calendar'),
    path('statistic/', login_required(Statistic.as_view()), name='bet_statistic'),
    path('ratings/', login_required(RatingsView.as_view()), name='bet_ratings'),
    path('ratings/football/', login_required(RatingFootballView.as_view()), name='bet_ratings_football'),

    path('profile/', login_required(ProfileView.as_view()), name='bet_profile'),

    path('sport_kind/create', login_required(SportKindCreateView.as_view()), name='create_sport_kind_form'),   # use modal form on bet_profile
    path('competition/create', login_required(CompetitionCreateView.as_view()), name='create_competition_form'),   # use modal form on bet_profile
    path('service/create', login_required(ServiceCreateView.as_view()), name='create_service_form'),   # use modal form on bet_profile

    path('sport_kind/delete/<int:id>/', login_required(SportKindDeleteView.as_view()), name='bet_sport_kind_delete'),
    path('competition/delete/<int:id>/', login_required(CompetitionDeleteView.as_view()), name='bet_competition_delete'),
    path('service/delete/<int:id>/', login_required(BettingServiceDeleteView.as_view()), name='bet_service_delete'),

]
