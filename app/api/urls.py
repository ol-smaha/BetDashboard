from django.urls import path

from api.views import BetBaseApiListView, BetBaseApiDetailView, BetFootballApiDetailView, BetFootballApiListView, \
   FootballTeamApiListView, FootballTeamApiDetailView, FootballCompetitionApiListView, FootballCompetitionApiDetailView, \
   BetBaseApiCreateView, BetBaseApiDeleteView, BetBaseApiUpdateView

urlpatterns = [
   path('bet/', BetBaseApiListView.as_view()),
   path('bet/<int:pk>/', BetBaseApiDetailView.as_view()),
   path('bet/create/', BetBaseApiCreateView.as_view()),
   path('bet/update/<int:pk>/', BetBaseApiUpdateView.as_view()),
   path('bet/delete/<int:pk>/', BetBaseApiDeleteView.as_view()),

   path('bet-football/', BetFootballApiListView.as_view()),
   path('bet-football/<int:pk>/', BetFootballApiDetailView.as_view()),

   path('team/', FootballTeamApiListView.as_view()),
   path('team/<int:pk>/', FootballTeamApiDetailView.as_view()),

   path('competition/', FootballCompetitionApiListView.as_view()),
   path('competition/<int:pk>/', FootballCompetitionApiDetailView.as_view()),

]
