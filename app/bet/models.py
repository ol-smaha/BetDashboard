from decimal import Decimal

from django.db import models
from django.apps import apps

from bet.constants import (BetResultEnum, GameStatusEnum, BetFootballTypeEnum,
                           TeamCategoryEnum, LiveTypeEnum, BetFootballPredictionEnum)
from users.models import CustomUser


current_request = None


class Country(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code2 = models.CharField(max_length=2, null=True, blank=True)
    code3 = models.CharField(max_length=4, null=True, blank=True)
    flag_code = models.CharField(max_length=8, null=True, blank=True)

    @classmethod
    def name_choices(cls):
        qs = cls.objects.all().values_list('name', flat=True).distinct()
        choices = tuple([(name, name) for name in qs])
        return choices

    def __str__(self):
        return f"{self.name}"


class SportKind(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='sport_kinds')
    name = models.CharField(max_length=128)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='sport kind name and user unique'),
        ]

    @classmethod
    def name_choices(cls):
        qs = cls.objects.all()
        try:
            if current_request and current_request.user:
                qs = qs.filter(user=current_request.user)
        except:
            pass
        choices = tuple([(_id, name) for _id, name in qs.values_list('id', 'name')])
        return choices

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(max_length=128)
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
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='competitions')
    name = models.CharField(max_length=128)
    sport_kind = models.ForeignKey(to=SportKind, on_delete=models.SET_NULL,
                                   related_name='competitions', null=True, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.SET_NULL,
                                related_name='competitions', null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='competition name and user unique'),
        ]

    @classmethod
    def name_choices(cls):
        qs = cls.objects.all().values_list('name', flat=True)
        try:
            if current_request and current_request.user:
                qs = qs.filter(user=current_request.user)

        except:
            pass
        choices = tuple([(_id, name) for _id, name in qs.values_list('id', 'name')])
        return choices

    def __str__(self):
        return f"{self.name}"


class BettingService(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='services')
    name = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='service name and user unique'),
        ]

    @classmethod
    def name_choices(cls):
        qs = cls.objects.all()
        try:
            if current_request and current_request.user:
                qs = qs.filter(user=current_request.user)
        except:
            pass
        choices = tuple([(_id, name) for _id, name in qs.values_list('id', 'name')])
        return choices

    def __str__(self):
        return f"{self.name}"


class BetBase(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='bets')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    coefficient = models.DecimalField(max_digits=10, decimal_places=2)
    result = models.CharField(max_length=32, choices=BetResultEnum.choices())
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sport_kind = models.ForeignKey(to=SportKind, on_delete=models.SET_NULL,
                                   related_name='bets', null=True, blank=True)
    date_game = models.DateField(null=True, blank=True)
    is_favourite = models.BooleanField(default=False)
    live_type = models.CharField(max_length=32, blank=True, null=True, choices=LiveTypeEnum.choices())
    betting_service = models.ForeignKey(to=BettingService, on_delete=models.SET_NULL,
                                        related_name='bets', null=True, blank=True)

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

    def save_to_child_model(self, child_model_name, *args, **kwargs):
        is_saved = kwargs.get('is_saved', False)
        data = {}

        for field in self._meta.fields:
            if field.name == 'id':
                continue

            value = field.value_from_object(self)
            field_name = f'{field.name}_id' if isinstance(field, models.ForeignKey) else field.name
            data.update({field_name: value})

        _ChildModel = apps.get_model(app_label="bet", model_name=child_model_name)
        child_instance = _ChildModel(**data)
        child_instance.save(is_saved=is_saved)

    def save(self, *args, **kwargs):
        is_saved = kwargs.get('is_saved', False)
        if self.profit is None:
            self.profit = self.calculate_profit()

        if not getattr(self, 'betfootball', None) and self.sport_kind and self.sport_kind.name == 'Футбол' and not is_saved:
            self.save_to_child_model('BetFootball', is_saved=True)
        else:
            if kwargs.get('is_saved'):
                kwargs.pop('is_saved')
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.result} - {self.coefficient} - {self.amount}"


class BetFootball(BetBase):
    team_home = models.ForeignKey(to=Team, on_delete=models.SET_NULL,
                                  related_name='home_bets', null=True, blank=True)
    team_guest = models.ForeignKey(to=Team, on_delete=models.SET_NULL,
                                   related_name='guest_bets', null=True, blank=True)
    prediction = models.CharField(max_length=128, choices=BetFootballPredictionEnum.choices(),
                                  null=True, blank=True)
    bet_type = models.CharField(max_length=64, choices=BetFootballTypeEnum.choices(),
                                null=True, blank=True, default=BetFootballTypeEnum.UNKNOWN)
    competition = models.ForeignKey(to=CompetitionBase, on_delete=models.SET_NULL,
                                    related_name='bets_football', null=True, blank=True)
    game_status = models.CharField(max_length=16, choices=GameStatusEnum.choices(),
                                   null=True, blank=True, default=GameStatusEnum.UNKNOWN)

    def save(self, *args, **kwargs):
        self.sport_kind, _ = SportKind.objects.get_or_create(user=self.user, name='Футбол')
        if self.bet_type == BetFootballTypeEnum.UNKNOWN or not self.bet_type:
            if self.prediction:
                self.bet_type = BetFootballTypeEnum.get_value_by_bet(self.prediction)
        super().save(*args, **kwargs)




