from django.urls import path

from api.views import BetBaseApiListView, BetBaseApiDetailView

urlpatterns = [
   path('bet/', BetBaseApiListView.as_view()),
   path('bet/<int:pk>/', BetBaseApiDetailView.as_view()),

]
