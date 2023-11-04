import datetime
import random

from django.contrib.auth import get_user_model
from django.utils.timezone import now

from bet.constants import BetVariant, BetResultEnum
from bet.models import SportKind, BetBase

UserModel = get_user_model()


def generate_bets():
    BetBase.objects.all().delete()
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


