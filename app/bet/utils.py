import datetime
import random

from django.contrib.auth import get_user_model

from bet.constants import BetVariant, BetResultEnum, BetTypeEnum, GameStatusEnum, TeamCategoryEnum, \
    CompetitionFootballCategoryEnum
from bet.models import SportKind, BetBase, BetFootball, Team, CompetitionFootball, Country

UserModel = get_user_model()


def generate_bets():
    # BetBase.objects.all().delete()
    sport_kind = SportKind.objects.get(name="Футбол")

    for year in range(2020, 2024):
        for month in range(1, 13):
            for day in range(1, 29):
                bet_count = random.randrange(3, 6)
                for i in range(bet_count):
                    user = UserModel.objects.get(username='admin')
                    bet = random.choice(BetVariant.values())
                    amount = random.randrange(100, 500)
                    coefficient = round(random.uniform(1.5, 2.5), 2)
                    result = random.choice(BetResultEnum.values())
                    date_game = datetime.date(year=year, month=month, day=day)
                    date_betting = date_game

                    bet = BetBase.objects.create(
                        user=user,
                        bet=bet,
                        amount=amount,
                        coefficient=coefficient,
                        result=result,
                        sport_kind=sport_kind,
                        date_game=date_game,
                        date_betting=date_betting
                    )
                    print(date_game)
                    del bet


def generate_football_bets():
    # BetFootball.objects.all().delete()
    sport_kind, _ = SportKind.objects.get_or_create(name="Футбол")
    country, _ = Country.objects.get_or_create(name='Іспанія')
    team_home, _ = Team.objects.get_or_create(
        name='Реал',
        defaults={
            'name_extended': 'ФК Реал Мадрид',
            'category': TeamCategoryEnum.CLUB,
            'sport_kind': sport_kind,
            'country': country,

        }
    )
    team_guest, _ = Team.objects.get_or_create(
        name='Барселона',
        defaults={
            'name_extended': 'ФК Барселона',
            'category': TeamCategoryEnum.CLUB,
            'sport_kind': sport_kind,
            'country': country,

        }
    )
    competition, _ = CompetitionFootball.objects.get_or_create(
        name='Ла Ліга',
        defaults={
            'category': CompetitionFootballCategoryEnum.CLUB,
            'sport_kind': sport_kind,
            'country': country,

        }
    )

    for year in range(2023, 2024):
        for month in range(1, 13):
            for day in range(1, 29):
                bet_count = random.randrange(2, 4)
                for i in range(bet_count):
                    user = UserModel.objects.get(username='admin')
                    bet = random.choice(BetVariant.values())
                    amount = random.randrange(100, 500)
                    coefficient = round(random.uniform(1.5, 2.5), 2)
                    result = random.choice(BetResultEnum.values())
                    date_game = datetime.date(year=year, month=month, day=day)
                    date_betting = date_game
                    bet_type = random.choice(BetTypeEnum.values())
                    game_status = random.choice(GameStatusEnum.values())

                    bet = BetFootball.objects.create(
                        user=user,
                        bet=bet,
                        amount=amount,
                        coefficient=coefficient,
                        result=result,
                        sport_kind=sport_kind,
                        date_game=date_game,
                        date_betting=date_betting,
                        bet_type=bet_type,
                        game_status=game_status,
                        team_home=team_home,
                        team_guest=team_guest,
                        competition=competition,
                    )
                    print(date_game)
                    del bet


