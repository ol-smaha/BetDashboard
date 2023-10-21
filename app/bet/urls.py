from django.urls import path

from bet.views import BetHistory

urlpatterns = [
    path('history/', BetHistory.as_view(), name='bet_history')
]
