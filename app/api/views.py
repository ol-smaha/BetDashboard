from rest_framework import generics

from api.serializers import BetBaseSerializer
from bet.models import BetBase


class BetBaseApiListView(generics.ListAPIView):
    queryset = BetBase.objects.all().order_by('amount', 'id')
    serializer_class = BetBaseSerializer


class BetBaseApiDetailView(generics.RetrieveAPIView):
    queryset = BetBase.objects.all().order_by('amount', 'id')
    serializer_class = BetBaseSerializer
