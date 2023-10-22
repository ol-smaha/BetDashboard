from django.urls import path

from bet.views import BetHistory, Graphs

urlpatterns = [
    path('history/', BetHistory.as_view(), name='bet_history'),
    path('graphs/', Graphs.as_view(), name='graphs'),
]
