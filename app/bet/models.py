from decimal import Decimal

from django.db import models

from bet.constants import (BetResultEnum, GameStatusEnum, BetTypeEnum,
                           CompetitionFootballCategoryEnum, TeamCategoryEnum, BetPredictionEnum, LiveTypeEnum)
from users.models import CustomUser


class Country(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code2 = models.CharField(max_length=2, null=True, blank=True)
    code3 = models.CharField(max_length=4, null=True, blank=True)
    flag_code = models.CharField(max_length=4, null=True, blank=True)

    @classmethod
    def name_choices(cls):
        qs = cls.objects.all().values_list('name', flat=True).distinct()
        choices = tuple([(name, name) for name in qs])
        return choices

    def __str__(self):
        return f"{self.name}"


class SportKind(models.Model):
    name = models.CharField(unique=True, max_length=128)
    is_active = models.BooleanField(default=False)

    @classmethod
    def name_choices(cls):
        qs = cls.objects.filter(is_active=True).values_list('name', flat=True).distinct()
        choices = tuple([(name, name) for name in qs])
        return choices

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    name_extended = models.CharField(max_length=256, unique=True)
    category = models.CharField(max_length=32, choices=TeamCategoryEnum.choices(),
                                default=TeamCategoryEnum.UNKNOWN)
    sport_kind = models.ForeignKey(to=SportKind, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.SET_NULL,
                                related_name='teams', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class CompetitionBase(models.Model):
    name = models.CharField(max_length=128, unique=True)
    sport_kind = models.ForeignKey(to=SportKind, on_delete=models.SET_NULL,
                                   related_name='competitions', null=True, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.SET_NULL,
                                related_name='competitions', null=True, blank=True)

    @classmethod
    def name_choices(cls):
        qs = cls.objects.all().values_list('name', flat=True).distinct()
        choices = tuple([(name, name) for name in qs])
        return choices

    def __str__(self):
        return f"{self.name}"


class CompetitionFootball(CompetitionBase):
    category = models.CharField(max_length=32, choices=CompetitionFootballCategoryEnum.choices(),
                                default=CompetitionFootballCategoryEnum.UNKNOWN)


class BetBase(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='bets')
    prediction = models.CharField(max_length=128, choices=BetPredictionEnum.choices())
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    coefficient = models.DecimalField(max_digits=10, decimal_places=2)
    result = models.CharField(max_length=32, choices=BetResultEnum.choices())
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sport_kind = models.ForeignKey(to=SportKind, on_delete=models.SET_NULL,
                                   related_name='bets', null=True, blank=True)
    date_game = models.DateField(null=True, blank=True)
    is_favourite = models.BooleanField(default=False)
    live_type = models.CharField(max_length=32, blank=True, null=True, choices=LiveTypeEnum.choices())

    def calculate_profit(self):
        profit = Decimal('0.00')
        if self.result == BetResultEnum.WIN:
            profit = round(Decimal(self.amount * self.coefficient - self.amount), 2)
        elif self.result == BetResultEnum.LOSE:
            profit = Decimal(f'-{self.amount}')
        return profit

    def change_is_favourite(self, commit=True):
        self.is_favourite = not self.is_favourite
        if commit:
            self.save()

    def save(self, *args, **kwargs):
        if self.profit is None:
            self.profit = self.calculate_profit()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.result} - {self.coefficient} - {self.amount}"


class BetFootball(BetBase):
    team_home = models.ForeignKey(to=Team, on_delete=models.SET_NULL,
                                  related_name='home_bets', null=True, blank=True)
    team_guest = models.ForeignKey(to=Team, on_delete=models.SET_NULL,
                                   related_name='guest_bets', null=True, blank=True)
    bet_type = models.CharField(max_length=64, choices=BetTypeEnum.choices(),
                                default=BetTypeEnum.UNKNOWN)
    competition = models.ForeignKey(to=CompetitionFootball, on_delete=models.SET_NULL,
                                    related_name='bets_football', null=True, blank=True)
    game_status = models.CharField(max_length=16, choices=GameStatusEnum.choices(),
                                   default=GameStatusEnum.UNKNOWN)

    def save(self, *args, **kwargs):
        sport_kind, _ = SportKind.objects.get_or_create(name='Футбол')
        self.sport_kind = sport_kind
        if self.bet_type == BetTypeEnum.UNKNOWN or not self.bet_type:
            if self.prediction:
                self.bet_type = BetTypeEnum.get_value_by_bet(self.prediction)
        super().save(*args, **kwargs)
