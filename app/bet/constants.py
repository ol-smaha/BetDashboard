from enum import StrEnum


class BetResultEnum(StrEnum):
    WIN = 'Виграш'
    DRAWN = 'Повернення'
    LOSE = 'Програш'
    UNKNOWN = 'Невідомо'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res

    @classmethod
    def values(cls):
        res = [e.value for e in cls]
        return res


class BetPredictionEnum(StrEnum):
    EXPRESS = 'Експрес'
    W1 = 'П1'
    X = 'Нічия'
    W2 = 'П2'
    WX1 = '1-Х'
    NOT_X = '1-2'
    WX2 = '2-Х'
    O_Z = 'ОЗ'
    TO_0_5 = 'ТБ 0.5'
    TO_1_0 = 'ТБ 1.0'
    TO_1_5 = 'ТБ 1.5'
    TO_2_0 = 'ТБ 2.0'
    TO_2_5 = 'ТБ 2.5'
    TO_3_0 = 'ТБ 3.0'
    TO_3_5 = 'ТБ 3.5'
    TO_4_0 = 'ТБ 4.0'
    TO_4_5 = 'ТБ 4.5'
    TO_5_0 = 'ТБ 5.0'
    TO_5_5 = 'ТБ 5.5'
    TU_0_5 = 'ТМ 0.5'
    TU_1_0 = 'ТМ 1.0'
    TU_1_5 = 'ТМ 1.5'
    TU_2_0 = 'ТМ 2.0'
    TU_2_5 = 'ТМ 2.5'
    TU_3_0 = 'ТМ 3.0'
    TU_3_5 = 'ТМ 3.5'
    TU_4_0 = 'ТМ 4.0'
    TU_4_5 = 'ТМ 4.5'
    TU_5_0 = 'ТМ 5.0'
    TU_5_5 = 'ТМ 5.5'
    F1_0_0 = 'Ф1 (0)'
    F1_MINUS_0_5 = 'Ф1 (-0.5)'
    F1_MINUS_1_0 = 'Ф1 (-1.0)'
    F1_MINUS_1_5 = 'Ф1 (-1.5)'
    F1_MINUS_2_0 = 'Ф1 (-2.0)'
    F1_MINUS_2_5 = 'Ф1 (-2.5)'
    F1_MINUS_3_0 = 'Ф1 (-3.0)'
    F2_0_0 = 'Ф2 (0)'
    F2_MINUS_0_5 = 'Ф2 (-0.5)'
    F2_MINUS_1_0 = 'Ф2 (-1.0)'
    F2_MINUS_1_5 = 'Ф2 (-1.5)'
    F2_MINUS_2_0 = 'Ф2 (-2.0)'
    F2_MINUS_2_5 = 'Ф2 (-2.5)'
    F2_MINUS_3_0 = 'Ф2 (-3.0)'
    F1_PLUS_0_5 = 'Ф1 (+0.5)'
    F1_PLUS_1_0 = 'Ф1 (+1.0)'
    F1_PLUS_1_5 = 'Ф1 (+1.5)'
    F1_PLUS_2_0 = 'Ф1 (+2.0)'
    F1_PLUS_2_5 = 'Ф1 (+2.5)'
    F1_PLUS_3_0 = 'Ф1 (+3.0)'
    F2_PLUS_0_5 = 'Ф2 (+0.5)'
    F2_PLUS_1_0 = 'Ф2 (+1.0)'
    F2_PLUS_1_5 = 'Ф2 (+1.5)'
    F2_PLUS_2_0 = 'Ф2 (+2.0)'
    F2_PLUS_2_5 = 'Ф2 (+2.5)'
    F2_PLUS_3_0 = 'Ф2 (+3.0)'
    OTHER = 'Інше'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res

    @classmethod
    def values(cls):
        res = [e.value for e in cls]
        return res

    @classmethod
    def items(cls):
        res = [e.value for e in cls]
        return res


class BetTypeEnum(StrEnum):
    WDL = 'П1-Х-П2'
    WX = '1Х-12-Х2'
    FORA = 'Фора'
    TOTAL = 'Тотал'
    EXPRESS = 'Експрес'
    UNKNOWN = 'Інше'

    @classmethod
    def get_value_by_bet(cls, prediction):
        print(prediction)
        print(cls.prediction_type_dict().get(prediction, cls.UNKNOWN))
        return cls.prediction_type_dict().get(prediction, cls.UNKNOWN)

    @classmethod
    def prediction_type_dict(cls):
        mapper = {
            cls.WDL: (
                BetPredictionEnum.W1,
                BetPredictionEnum.X,
                BetPredictionEnum.W2,
            ),
            cls.WX: (
                BetPredictionEnum.WX1,
                BetPredictionEnum.NOT_X,
                BetPredictionEnum.WX2,
            ),
            cls.FORA: (
                BetPredictionEnum.F1_0_0,
                BetPredictionEnum.F1_MINUS_0_5,
                BetPredictionEnum.F1_MINUS_1_0,
                BetPredictionEnum.F1_MINUS_1_5,
                BetPredictionEnum.F1_MINUS_2_0,
                BetPredictionEnum.F1_MINUS_2_5,
                BetPredictionEnum.F1_MINUS_3_0,
                BetPredictionEnum.F2_0_0,
                BetPredictionEnum.F2_MINUS_0_5,
                BetPredictionEnum.F2_MINUS_1_0,
                BetPredictionEnum.F2_MINUS_1_5,
                BetPredictionEnum.F2_MINUS_2_0,
                BetPredictionEnum.F2_MINUS_2_5,
                BetPredictionEnum.F2_MINUS_3_0,
                BetPredictionEnum.F1_PLUS_0_5,
                BetPredictionEnum.F1_PLUS_1_0,
                BetPredictionEnum.F1_PLUS_1_5,
                BetPredictionEnum.F1_PLUS_2_0,
                BetPredictionEnum.F1_PLUS_2_5,
                BetPredictionEnum.F1_PLUS_3_0,
                BetPredictionEnum.F2_PLUS_0_5,
                BetPredictionEnum.F2_PLUS_1_0,
                BetPredictionEnum.F2_PLUS_1_5,
                BetPredictionEnum.F2_PLUS_2_0,
                BetPredictionEnum.F2_PLUS_2_5,
                BetPredictionEnum.F2_PLUS_3_0,
            ),
            cls.TOTAL: (
                BetPredictionEnum.TO_0_5,
                BetPredictionEnum.TO_1_0,
                BetPredictionEnum.TO_1_5,
                BetPredictionEnum.TO_2_0,
                BetPredictionEnum.TO_2_5,
                BetPredictionEnum.TO_3_0,
                BetPredictionEnum.TO_3_5,
                BetPredictionEnum.TO_4_0,
                BetPredictionEnum.TO_4_5,
                BetPredictionEnum.TO_5_0,
                BetPredictionEnum.TO_5_5,
                BetPredictionEnum.TU_0_5,
                BetPredictionEnum.TU_1_0,
                BetPredictionEnum.TU_1_5,
                BetPredictionEnum.TU_2_0,
                BetPredictionEnum.TU_2_5,
                BetPredictionEnum.TU_3_0,
                BetPredictionEnum.TU_3_5,
                BetPredictionEnum.TU_4_0,
                BetPredictionEnum.TU_4_5,
                BetPredictionEnum.TU_5_0,
                BetPredictionEnum.TU_5_5,
            ),
            cls.EXPRESS: (
                BetPredictionEnum.EXPRESS,
            ),
        }
        reverse_dict = {}
        for bet_type, bet_predictions in mapper.items():
            for prediction in bet_predictions:
                reverse_dict.update({prediction: bet_type})
        return reverse_dict

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res

    @classmethod
    def values(cls):
        res = [e.value for e in cls]
        return res


class GameStatusEnum(StrEnum):
    OFFICIAL = 'OFFICIAL'
    FRIENDLY = 'FRIENDLY'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res

    @classmethod
    def values(cls):
        res = [e.value for e in cls]
        return res


class LiveTypeEnum(StrEnum):
    LIVE = 'Лайв'
    PREMATCH = 'Прематч'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res


class TeamCategoryEnum(StrEnum):
    CLUB = 'CLUB'
    NATIONAL = 'NATIONAL'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res


class CompetitionFootballCategoryEnum(StrEnum):
    CLUB = 'CLUB'
    NATIONAL = 'NATIONAL'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res


BET_BASE_TABLE_FIELD_NAMES = {
    'date_game': 'Дата',
    'prediction': 'Прогноз',
    'amount': 'Сума',
    'coefficient': 'Коефіцієнт',
    'result': 'Результат ставки',
    'profit': 'Прибуток',
    'sport_kind': 'Спорт',
    'live_type': 'Момент ставки',
    'is_favourite': '⭐',
    'action_delete': '☒',
}

BET_FOOTBALL_FIELDS_NAMES = {
    'date_game': 'Date Of Game',
    'prediction': 'Bet',
    'amount': 'Amount',
    'coefficient': 'Coefficient',
    'result': 'Bet Result',
    'live_type': 'Live Type',
    'profit': 'Profit',
    'team_home': 'Team Home',
    'team_guest': 'Team Guess',
    'bet_type': 'Bet Type',
    'competition': 'Competition',
    'game_status': 'Game Status',
    'is_home_guest': 'Is Home Guest',
    'is_favourite': '⭐',
    'action_delete': '☒',
}


DEFAULT_MORRIS_CHART_COLORS = [
    '#07F78A ', #файний салатовий
    '#168251', #зелений як ліс
    '#66CA9C', #зелений пастельний
    '#FF5656', #червоний термоядерний, але лайтово
    '#EF2828', #термоядерний черновий
    '#F89A46', #оранжевий не термоядерний
    '#FEDA53', #жовтий нормальний
    '#FEE589', #жовтий пастельний
    '#85FAE1', #голубеньний
    '#39BDA1', #голубо-зелений темнуватий
    '#66B5DD', #колір як небо
    '#426DE8', #синій
    '#A96DFA', #фіолетовий
]

CHART_ONE_LINE_COLORS = [
    '#236995',
]

CHART_ONE_LINE_WITH_COUNT_COLORS = [
    '#bfbfbd',  # count line - grey
    '#236995',
]

OTHER_COLORS = [
    '#bfbfbd',   # count line - grey
    '#236995',
    '#077373',
    '#8b74ff',
    '#ce4765',
    '#356734',
    '#66330c',
    '#479a9a',
]

BET_RESULT_COLORS = [
    '#6fce68',
    '#ebbf3b',
    '#ff6161',
    '#bfbfbd',
]


def get_result_color(result):
    colors = {
        BetResultEnum.WIN: '#6fce68',
        BetResultEnum.DRAWN: '#ebbf3b',
        BetResultEnum.LOSE: '#ff6161',
        BetResultEnum.UNKNOWN: '#bfbfbd',
    }
    return colors.get(result, '#828282')


BET_BASE_ORDERING_FIELDS_CHOICES = (
    ('date_game', 'Дата події'),
    ('prediction', 'Прогноз'),
    ('amount', 'Сума ставки'),
    ('coefficient', 'Коефіцієнт'),
    ('result', 'Результат ставки'),
    ('profit', 'Профіт'),
    ('sport_kind', 'Вид спорту'),
    ('is_favourite', 'Улюблене'),

)

BOOL_FIELD_CHOICES = (
    (True, 'Так'),
    (False, 'Ні'),
)


class ChartDateType(StrEnum):
    NOW = 'Поточний місяць'
    LAST_30_DAYS = 'Останні 30 діб'
    MONTHS = 'По місяцях'
    YEARS = 'По роках'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res

    @classmethod
    def values(cls):
        res = [e.value for e in cls]
        return res

    @classmethod
    def items(cls):
        res = [e.value for e in cls]
        return res
