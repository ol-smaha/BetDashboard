from django.urls import path

from api.views import BetBaseApiListView, BetBaseApiDetailView, BetFootballApiDetailView, BetFootballApiListView, \
   FootballTeamApiListView, FootballTeamApiDetailView, FootballCompetitionApiListView, FootballCompetitionApiDetailView

urlpatterns = [
   path('bet/', BetBaseApiListView.as_view()),
   path('bet/<int:pk>/', BetBaseApiDetailView.as_view()),
   path('bet-football/', BetFootballApiListView.as_view()),
   path('bet-football/<int:pk>/', BetFootballApiDetailView.as_view()),
   path('team/', FootballTeamApiListView.as_view()),
   path('team/<int:pk>/', FootballTeamApiDetailView.as_view()),
   path('competition/', FootballCompetitionApiListView.as_view()),
   path('competition/<int:pk>/', FootballCompetitionApiDetailView.as_view()),

]
