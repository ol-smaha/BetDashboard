from rest_framework import serializers

from bet.models import BetBase, SportKind, BettingService, BetFootball, Team, CompetitionBase, Country


class SportKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportKind
        fields = ['user', 'id', 'name']


class BettingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BettingService
        fields = ['user', 'id', 'name']


class BetBaseSerializer(serializers.ModelSerializer):
    sport_kind = SportKindSerializer()
    betting_service = BettingServiceSerializer()

    class Meta:
        model = BetBase
        fields = ['user', 'id', 'amount', 'coefficient',
                  'result', 'profit', 'date_game',
                  'is_favourite', 'live_type', 'sport_kind', 'betting_service']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code2', 'code3', 'flag_code']


class TeamSerializer(serializers.ModelSerializer):
    sport_kind = SportKindSerializer()
    country = CountrySerializer()

    class Meta:
        model = Team
        fields = ['name', 'id', 'name_extended', 'category', 'sport_kind', 'country']


class CompetitionSerializer(serializers.ModelSerializer):
    sport_kind = SportKindSerializer()
    country = CountrySerializer()

    class Meta:
        model = CompetitionBase
        fields = ['user', 'id', 'name', 'sport_kind', 'country']


class BetFootballSerializer(serializers.ModelSerializer):
    sport_kind = SportKindSerializer()
    betting_service = BettingServiceSerializer()
    team_home = TeamSerializer()
    team_guest = TeamSerializer()
    competition = CompetitionSerializer()

    class Meta:
        model = BetFootball
        fields = ['user', 'id', 'amount', 'coefficient',
                  'result', 'profit', 'date_game',
                  'is_favourite', 'live_type', 'sport_kind', 'betting_service', 'team_home', 'team_guest', 'prediction',
                  'bet_type', 'competition', 'game_status']
