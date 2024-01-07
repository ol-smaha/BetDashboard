import csv
import datetime
import random

from django.contrib.auth import get_user_model

from bet.constants import BetFootballPredictionEnum, BetResultEnum, BetFootballTypeEnum, GameStatusEnum, \
    TeamCategoryEnum, LiveTypeEnum, COUNTRIES, DEFAULT_SPORT_KINDS, DEFAULT_BETTING_SERVICES, \
    DEFAULT_COMPETITIONS_FOOTBALL
from bet.models import SportKind, BetBase, BetFootball, Team, Country, BettingService, CompetitionBase
from users.models import Notification

UserModel = get_user_model()


def reverse_dict(dct):
    try:
        reverse = {}
        for key, val in dct.items():
            reverse.update({val: key})
        return reverse
    except:
        return dct


def generate_bets():
    BetBase.objects.all().delete()
    user = UserModel.objects.get(username='admin')
    sport_kind, _ = SportKind.objects.get_or_create(user=user, name="Футбол")

    for year in range(2020, 2024):
        for month in range(1, 13):
            for day in range(1, 29):
                bet_count = random.randrange(3, 6)
                for i in range(bet_count):
                    amount = random.randrange(100, 300)
                    coefficient = round(random.uniform(1.5, 2.2), 2)
                    result = random.choice(BetResultEnum.values())
                    date_game = datetime.date(year=year, month=month, day=day)

                    bet = BetBase.objects.create(
                        user=user,
                        amount=amount,
                        coefficient=coefficient,
                        result=result,
                        sport_kind=sport_kind,
                        date_game=date_game,
                    )
                    print(date_game)
                    del bet


def generate_football_bets():
    BetFootball.objects.all().delete()
    user = UserModel.objects.get(username='admin')

    sport_kind_football, _ = SportKind.objects.get_or_create(user=user, name="Футбол")
    sport_kind_basketball, _ = SportKind.objects.get_or_create(user=user, name="Баскетбол")
    sport_kind_tennis, _ = SportKind.objects.get_or_create(user=user, name="Теніс")

    country_spain, _ = Country.objects.get_or_create(name='Іспанія', flag_code='es')
    country_england, _ = Country.objects.get_or_create(name='Англія', flag_code='gb')
    country_italy, _ = Country.objects.get_or_create(name='Італія', flag_code='it')

    service_vbet, _ = BettingService.objects.get_or_create(user=user, name='Vbet')
    service_favbet, _ = BettingService.objects.get_or_create(user=user, name='FavBet')

    team_real, _ = Team.objects.get_or_create(
        name='Реал',
        defaults={
            'name_extended': 'ФК Реал Мадрид',
            'category': TeamCategoryEnum.CLUB,
            'sport_kind': sport_kind_football,
            'country': country_spain,

        }
    )
    team_barcelona, _ = Team.objects.get_or_create(
        name='Барселона',
        defaults={
            'name_extended': 'ФК Барселона',
            'category': TeamCategoryEnum.CLUB,
            'sport_kind': sport_kind_football,
            'country': country_spain,

        }
    )
    competition, _ = CompetitionBase.objects.get_or_create(
        name='Ла Ліга',
        defaults={
            'sport_kind': sport_kind_football,
            'country': country_spain,

        }
    )

    for year in range(2023, 2024):
        for month in range(1, 13):
            for day in range(1, 29):
                bet_count = random.randrange(2, 4)
                for i in range(bet_count):
                    prediction = random.choice(BetFootballPredictionEnum.values())
                    amount = random.randrange(100, 300)
                    coefficient = round(random.uniform(1.5, 2.2), 2)
                    result = random.choice(BetResultEnum.values())
                    date_game = datetime.date(year=year, month=month, day=day)
                    bet_type = random.choice(BetFootballTypeEnum.values())
                    game_status = random.choice(GameStatusEnum.values())

                    bet = BetFootball.objects.create(
                        user=user,
                        prediction=prediction,
                        amount=amount,
                        coefficient=coefficient,
                        result=result,
                        sport_kind=sport_kind_football,
                        date_game=date_game,
                        bet_type=bet_type,
                        game_status=game_status,
                        team_home=team_real,
                        team_guest=team_barcelona,
                        competition=competition,
                        betting_service=random.choice([service_vbet, service_favbet]),
                        live_type=random.choice([LiveTypeEnum.LIVE, LiveTypeEnum.PREMATCH]),
                    )
                    print(date_game)
                    del bet


def create_default_countries():
    try:
        objs = []
        for name, data in COUNTRIES.items():
            objs.append(
                Country(
                    name=name,
                    code2=data.get('code_2'),
                    code3=data.get('code_3'),
                    flag_code=data.get('flag_code')
                )
            )
        Country.objects.bulk_create(objs, ignore_conflicts=True)
    except Exception as e:
        print(e)


def create_default_sport_kind(user):
    try:
        objs = []
        for name in DEFAULT_SPORT_KINDS:
            objs.append(SportKind(user=user, name=name))
        SportKind.objects.bulk_create(objs, ignore_conflicts=True)
    except Exception as e:
        print(e)


def create_default_betting_services(user):
    try:
        objs = []
        for name in DEFAULT_BETTING_SERVICES:
            objs.append(BettingService(user=user, name=name))
        BettingService.objects.bulk_create(objs, ignore_conflicts=True)
    except Exception as e:
        print(e)


def create_default_competitions_teams(user):
    with open('teams.csv') as csv_file:
        data = csv.DictReader(csv_file)
        sport_kind_obj, _ = SportKind.objects.get_or_create(user=user, name='Футбол')
        for row in data:
            country_name = row.get('country')
            competition_name = row.get('competition')
            teams = row.get('teams', '').split('\n')

            for team_name in teams:
                if country_name and competition_name and sport_kind_obj:
                    try:
                        country_obj, _ = Country.objects.get_or_create(name=country_name)
                        competition_obj, _ = CompetitionBase.objects.get_or_create(
                            user=user,
                            name=competition_name,
                            name_extended=f'{competition_name} ({country_name})',
                            sport_kind=sport_kind_obj,
                            country=country_obj,
                        )
                        # team_obj, _ = Team.objects.get_or_create(
                        #     name=team_name,
                        #     name_extended=f'{team_name} ({country_name})',
                        #     category=TeamCategoryEnum.CLUB,
                        #     sport_kind=sport_kind_obj,
                        #     country=country_obj,
                        # )
                    except Exception as e:
                        print(e)


def create_registration_notifications(user):
    try:
        message = ('Вітаємо у Bet Office.|Щоб дізнатись як користуватись сервісом скористайтесь розділом "Довідка".|'
                   'Рекомендуємо спочатку зайти в розділ "Налаштування"|(іконка "Користувач" вверху справа)| та відредагувати перелік своїх варіантів.|'
                   'Залишились питання - пишіть нам через форму "Зворотній зв`язок" або в Телеграм."')
        Notification.objects.create(
            user=user,
            message=message,
            is_active=True,
        )
    except Exception as e:
        print(e)


def user_data_setup(user):
    print('--- START user_data_setup')
    print('--- START create_default_betting_services')
    create_default_betting_services(user)
    print('--- START create_default_sport_kind')
    create_default_sport_kind(user)
    print('--- START create_default_competitions_teams')
    create_default_competitions_teams(user)
    print('--- FINISH user_data_setup')
