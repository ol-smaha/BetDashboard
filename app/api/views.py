from rest_framework import generics, viewsets, mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend


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
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['date_game', 'amount', 'coefficient', 'result', 'sport_kind__name', 'betting_service__name',
                       'is_favourite', 'live_type', 'profit']

    filterset_fields = {
        'result': ["in", "exact"],
        'sport_kind': ["in", "exact"],
        'betting_service': ["in", "exact"],
        'live_type': ["in", "exact"],
        'is_favourite': ["in", "exact"],
        'date_game': ['gte', 'lte'],
        'amount': ['gte', 'lte'],
        'coefficient': ['gte', 'lte'],

    }

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
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['team_home__name', 'team_guest__name']
    ordering_fields = ['date_game', 'amount', 'coefficient', 'result', 'sport_kind__name', 'betting_service__name',
                       'is_favourite', 'live_type', 'profit', 'team_home__name', 'team_guest__name', 'prediction',
                       'competition']
    filterset_fields = {
        'result': ["in", "exact"],
        'sport_kind': ["in", "exact"],
        'betting_service': ["in", "exact"],
        'live_type': ["in", "exact"],
        'is_favourite': ["in", "exact"],
        'date_game': ['gte', 'lte'],
        'amount': ['gte', 'lte'],
        'coefficient': ['gte', 'lte'],
        'team_home': ["in", "exact"],
        'team_guest': ["in", "exact"],
        'prediction': ["in", "exact"],
        'competition': ["in", "exact"],
        'bet_type': ["in", "exact"],
        'game_status': ["in", "exact"],

    }

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'name': ["in", "exact"],
        'name_extended': ["in", "exact"],
    }


class CompetitionViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    A simple ViewSet for viewing and editing bets.
    """
    queryset = CompetitionBase.objects.all()
    serializer_class = CompetitionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'name': ["in", "exact"],
        'name_extended': ["in", "exact"],
        'sport_kind': ["in", "exact"],
        'country': ["in", "exact"],
    }

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'name': ["in", "exact"],
    }


class SportKindViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    """
    A simple ViewSet for viewing and editing bets.
    """
    queryset = SportKind.objects.all()
    serializer_class = SportKindSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'name': ["in", "exact"],
    }



