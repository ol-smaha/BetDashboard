from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import BetBaseViewSet, BetFootballViewSet, TeamViewSet, CompetitionViewSet, BettingServiceViewSet, \
    SportKindViewSet

router = DefaultRouter()
router.register('bet', BetBaseViewSet, basename='bet'),
router.register('bet-football', BetFootballViewSet, basename='bet-football'),
router.register('team', TeamViewSet, basename='team'),
router.register('competition', CompetitionViewSet, basename='competition'),
router.register('service', BettingServiceViewSet, basename='service'),
router.register('sport-kind', SportKindViewSet, basename='sport-kind'),


bet_urlpatterns = router.urls


urlpatterns = [
   # path('bet/', BetBaseApiListView.as_view()),
   # path('bet/<int:pk>/', BetBaseApiDetailView.as_view()),
   # path('bet/create/', BetBaseApiCreateView.as_view()),
   # path('bet/update/<int:pk>/', BetBaseApiUpdateView.as_view()),
   # path('bet/delete/<int:pk>/', BetBaseApiDeleteView.as_view()),

   # path('bet-football/', BetFootballApiListView.as_view()),
   # path('bet-football/<int:pk>/', BetFootballApiDetailView.as_view()),
   # path('bet-football/create/', BetFootballApiCreateView.as_view()),
   # path('bet-football/update/<int:pk>/', BetFootballApiUpdateView.as_view()),
   # path('bet-football/delete/<int:pk>/', BetFootballApiDeleteView.as_view()),

   # path('team/', TeamApiListView.as_view()),
   # path('team/<int:pk>/', TeamApiDetailView.as_view()),
   # path('team/create/', TeamApiCreateView.as_view()),
   # path('team/update/<int:pk>/', TeamApiUpdateView.as_view()),
   # path('team/delete/<int:pk>/', TeamApiDeleteView.as_view()),

   # path('competition/', CompetitionApiListView.as_view()),
   # path('competition/<int:pk>/', CompetitionApiDetailView.as_view()),
   # path('competition/create/', CompetitionApiCreateView.as_view()),
   # path('competition/update/<int:pk>/', CompetitionApiUpdateView.as_view()),
   # path('competition/delete/<int:pk>/', CompetitionApiDeleteView.as_view()),

]

urlpatterns.extend(bet_urlpatterns)
