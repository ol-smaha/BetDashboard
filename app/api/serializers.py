from rest_framework import serializers

from bet.models import BetBase, SportKind


class SportKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportKind
        fields = ['user', 'id', 'name']


class BetBaseSerializer(serializers.ModelSerializer):
    sport_kind = SportKindSerializer()
    betting_service = serializers.CharField(source='betting_service.name', allow_null=True, allow_blank=True)

    class Meta:
        model = BetBase
        fields = ['user', 'id', 'amount', 'coefficient',
                  'result', 'profit', 'date_game',
                  'is_favourite', 'live_type', 'sport_kind', 'betting_service']
