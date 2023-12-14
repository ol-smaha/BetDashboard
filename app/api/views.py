from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import BetBaseSerializer, BetFootballSerializer, TeamSerializer, CompetitionSerializer, \
    BetBaseCreateSerializer, BetFootballCreateSerializer, TeamCreateSerializer, CompetitionCreateSerializer, \
    BettingServiceSerializer, SportKindSerializer
from bet.models import BetBase, BetFootball, Team, CompetitionBase, BettingService, SportKind


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


class BetFootballViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    A simple ViewSet for viewing and editing bets.
    """
    queryset = BetFootball.objects.all()
    serializer_class = BetFootballSerializer

    def get_serializer_class(self):
        print(self.action)
        if self.action in ['create', 'update', 'partial_update']:
            return BetFootballCreateSerializer
        else:
            return self.serializer_class


class TeamViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    """
    A simple ViewSet for viewing and editing bets.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class CompetitionViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    A simple ViewSet for viewing and editing bets.
    """
    queryset = CompetitionBase.objects.all()
    serializer_class = CompetitionSerializer

    def get_serializer_class(self):
        print(self.action)
        if self.action in ['create', 'update', 'partial_update']:
            return CompetitionCreateSerializer
        else:
            return self.serializer_class


class BettingServiceViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    """
    A simple ViewSet for viewing and editing bets.
    """
    queryset = BettingService.objects.all()
    serializer_class = BettingServiceSerializer


class SportKindViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    """
    A simple ViewSet for viewing and editing bets.
    """
    queryset = SportKind.objects.all()
    serializer_class = SportKindSerializer



