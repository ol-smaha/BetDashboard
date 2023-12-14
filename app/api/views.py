from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import BetBaseSerializer, BetFootballSerializer, TeamSerializer, CompetitionSerializer, \
    BetBaseCreateSerializer, BetFootballCreateSerializer, TeamCreateSerializer, CompetitionCreateSerializer
from bet.models import BetBase, BetFootball, Team, CompetitionBase


class BetBaseViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """
    A simple ViewSet for viewing and editing bets.
    """
    queryset = BetBase.objects.all()
    serializer_class = BetBaseSerializer

    def get_serializer_class(self):
        print(self.action)
        if self.action in ['create', 'update', 'partial_update']:
            return BetBaseCreateSerializer
        else:
            return self.serializer_class


class BetBaseApiListView(generics.ListAPIView):
    queryset = BetBase.objects.all().order_by('amount', 'id')
    serializer_class = BetBaseSerializer


class BetBaseApiDetailView(generics.RetrieveAPIView):
    queryset = BetBase.objects.all().order_by('amount', 'id')
    serializer_class = BetBaseSerializer


class BetBaseApiCreateView(generics.CreateAPIView):
    queryset = BetBase.objects.all().order_by('amount', 'id')
    serializer_class = BetBaseCreateSerializer


class BetBaseApiUpdateView(generics.UpdateAPIView):
    queryset = BetBase.objects.all().order_by('amount', 'id')
    serializer_class = BetBaseCreateSerializer


class BetBaseApiDeleteView(generics.DestroyAPIView):
    queryset = BetBase.objects.all().order_by('amount', 'id')


class BetFootballApiListView(generics.ListAPIView):
    queryset = BetFootball.objects.all().order_by('amount', 'id')
    serializer_class = BetFootballSerializer


class BetFootballApiDetailView(generics.RetrieveAPIView):
    queryset = BetFootball.objects.all().order_by('amount', 'id')
    serializer_class = BetFootballSerializer


class BetFootballApiCreateView(generics.CreateAPIView):
    queryset = BetFootball.objects.all().order_by('amount', 'id')
    serializer_class = BetFootballCreateSerializer


class BetFootballApiUpdateView(generics.UpdateAPIView):
    queryset = BetFootball.objects.all().order_by('amount', 'id')
    serializer_class = BetFootballCreateSerializer


class BetFootballApiDeleteView(generics.DestroyAPIView):
    queryset = BetFootball.objects.all().order_by('amount', 'id')


class TeamApiListView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamApiDetailView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamApiCreateView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamCreateSerializer


class TeamApiUpdateView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamCreateSerializer


class TeamApiDeleteView(generics.DestroyAPIView):
    queryset = Team.objects.all()


class CompetitionApiListView(generics.ListAPIView):
    queryset = CompetitionBase.objects.all()
    serializer_class = CompetitionSerializer


class CompetitionApiDetailView(generics.RetrieveAPIView):
    queryset = CompetitionBase.objects.all()
    serializer_class = CompetitionSerializer


class CompetitionApiCreateView(generics.CreateAPIView):
    queryset = CompetitionBase.objects.all()
    serializer_class = CompetitionCreateSerializer


class CompetitionApiUpdateView(generics.UpdateAPIView):
    queryset = CompetitionBase.objects.all()
    serializer_class = CompetitionCreateSerializer


class CompetitionApiDeleteView(generics.DestroyAPIView):
    queryset = CompetitionBase.objects.all()

