from django.db.models import Sum
from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import BetBaseSerializer, BetFootballSerializer, TeamSerializer, CompetitionSerializer, \
    BetBaseCreateSerializer, BetFootballCreateSerializer, TeamCreateSerializer, CompetitionCreateSerializer, \
    BettingServiceSerializer, SportKindSerializer, BetStatisticSerializer
from bet.constants import BetResultEnum
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
                       'is_favourite', 'is_live_type', 'profit']

    filterset_fields = {
        'result': ["in", "exact"],
        'sport_kind': ["in", "exact"],
        'betting_service': ["in", "exact"],
        'is_live_type': ["in", "exact"],
        'is_favourite': ["in", "exact"],
        'date_game': ['gte', 'lte'],
        'amount': ['gte', 'lte'],
        'coefficient': ['gte', 'lte'],

    }

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BetBaseCreateSerializer
        elif self.action in ['statistic']:
            return BetStatisticSerializer
        else:
            return self.serializer_class

    @action(detail=True, methods=['GET'])
    def change_is_favourite(self, request, pk=None):
        try:
            bet = self.get_object()
        except BetBase.DoesNotExist:
            return Response({"error": "Bet not found."}, status=404)

        bet.is_favourite = not bet.is_favourite
        bet.save()

        return Response({"message": "Bet marked as favorite."}, status=200)

    @action(detail=False, methods=['GET'])
    def statistic(self, request, pk=None):
        data = {}

        total_bets_count = self.get_queryset().count()
        total_bets_profit = self.get_queryset().aggregate(Sum('profit')).get('profit__sum') or 0.00
        total_bets_amount = self.get_queryset().aggregate(Sum('amount')).get('amount__sum') or 0.00
        if total_bets_amount > 0:
            total_bets_roi = round(float(total_bets_profit) * 100 / float(total_bets_amount), 2)
        else:
            total_bets_roi = 0.00
        res_win = self.get_queryset().filter(result=BetResultEnum.WIN).count()
        res_drawn = self.get_queryset().filter(result=BetResultEnum.DRAWN).count()
        res_lose = self.get_queryset().filter(result=BetResultEnum.LOSE).count()
        res_unknown = self.get_queryset().filter(result=BetResultEnum.UNKNOWN).count()

        data.update({
            'total_bets_count': total_bets_count,
            'total_bets_profit': float(total_bets_profit),
            'total_bets_amount': float(total_bets_amount),
            'total_bets_roi': total_bets_roi,
            'res_win': res_win,
            'res_drawn': res_drawn,
            'res_lose': res_lose,
            'res_unknown': res_unknown,
        })

        return Response(data, status=200)


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
                       'is_favourite', 'is_live_type', 'profit', 'team_home__name', 'team_guest__name', 'prediction',
                       'competition']
    filterset_fields = {
        'result': ["in", "exact"],
        'sport_kind': ["in", "exact"],
        'betting_service': ["in", "exact"],
        'is_live_type': ["in", "exact"],
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



