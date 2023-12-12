from rest_framework import generics

from api.serializers import BetBaseSerializer, BetFootballSerializer, TeamSerializer, CompetitionSerializer
from bet.models import BetBase, BetFootball, Team, CompetitionBase


class BetBaseApiListView(generics.ListAPIView):
    queryset = BetBase.objects.all().order_by('amount', 'id')
    serializer_class = BetBaseSerializer


class BetBaseApiDetailView(generics.RetrieveAPIView):
    queryset = BetBase.objects.all().order_by('amount', 'id')
    serializer_class = BetBaseSerializer


class BetFootballApiListView(generics.ListAPIView):
    queryset = BetFootball.objects.all().order_by('amount', 'id')
    serializer_class = BetFootballSerializer


class BetFootballApiDetailView(generics.RetrieveAPIView):
    queryset = BetFootball.objects.all().order_by('amount', 'id')
    serializer_class = BetFootballSerializer


class FootballTeamApiListView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class FootballTeamApiDetailView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class FootballCompetitionApiListView(generics.ListAPIView):
    queryset = CompetitionBase.objects.all()
    serializer_class = CompetitionSerializer


class FootballCompetitionApiDetailView(generics.RetrieveAPIView):
    queryset = CompetitionBase.objects.all()
    serializer_class = CompetitionSerializer

