from enum import StrEnum


class BetResultEnum(StrEnum):
    WIN = 'Виграш'
    DRAWN = 'Повернення'
    LOSE = 'Програш'
    UNKNOWN = '-'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res

    @classmethod
    def values(cls):
        res = [e.value for e in cls]
        return res


class BetFootballPredictionEnum(StrEnum):
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


class BetFootballTypeEnum(StrEnum):
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
                BetFootballPredictionEnum.W1,
                BetFootballPredictionEnum.X,
                BetFootballPredictionEnum.W2,
            ),
            cls.WX: (
                BetFootballPredictionEnum.WX1,
                BetFootballPredictionEnum.NOT_X,
                BetFootballPredictionEnum.WX2,
            ),
            cls.FORA: (
                BetFootballPredictionEnum.F1_0_0,
                BetFootballPredictionEnum.F1_MINUS_0_5,
                BetFootballPredictionEnum.F1_MINUS_1_0,
                BetFootballPredictionEnum.F1_MINUS_1_5,
                BetFootballPredictionEnum.F1_MINUS_2_0,
                BetFootballPredictionEnum.F1_MINUS_2_5,
                BetFootballPredictionEnum.F1_MINUS_3_0,
                BetFootballPredictionEnum.F2_0_0,
                BetFootballPredictionEnum.F2_MINUS_0_5,
                BetFootballPredictionEnum.F2_MINUS_1_0,
                BetFootballPredictionEnum.F2_MINUS_1_5,
                BetFootballPredictionEnum.F2_MINUS_2_0,
                BetFootballPredictionEnum.F2_MINUS_2_5,
                BetFootballPredictionEnum.F2_MINUS_3_0,
                BetFootballPredictionEnum.F1_PLUS_0_5,
                BetFootballPredictionEnum.F1_PLUS_1_0,
                BetFootballPredictionEnum.F1_PLUS_1_5,
                BetFootballPredictionEnum.F1_PLUS_2_0,
                BetFootballPredictionEnum.F1_PLUS_2_5,
                BetFootballPredictionEnum.F1_PLUS_3_0,
                BetFootballPredictionEnum.F2_PLUS_0_5,
                BetFootballPredictionEnum.F2_PLUS_1_0,
                BetFootballPredictionEnum.F2_PLUS_1_5,
                BetFootballPredictionEnum.F2_PLUS_2_0,
                BetFootballPredictionEnum.F2_PLUS_2_5,
                BetFootballPredictionEnum.F2_PLUS_3_0,
            ),
            cls.TOTAL: (
                BetFootballPredictionEnum.TO_0_5,
                BetFootballPredictionEnum.TO_1_0,
                BetFootballPredictionEnum.TO_1_5,
                BetFootballPredictionEnum.TO_2_0,
                BetFootballPredictionEnum.TO_2_5,
                BetFootballPredictionEnum.TO_3_0,
                BetFootballPredictionEnum.TO_3_5,
                BetFootballPredictionEnum.TO_4_0,
                BetFootballPredictionEnum.TO_4_5,
                BetFootballPredictionEnum.TO_5_0,
                BetFootballPredictionEnum.TO_5_5,
                BetFootballPredictionEnum.TU_0_5,
                BetFootballPredictionEnum.TU_1_0,
                BetFootballPredictionEnum.TU_1_5,
                BetFootballPredictionEnum.TU_2_0,
                BetFootballPredictionEnum.TU_2_5,
                BetFootballPredictionEnum.TU_3_0,
                BetFootballPredictionEnum.TU_3_5,
                BetFootballPredictionEnum.TU_4_0,
                BetFootballPredictionEnum.TU_4_5,
                BetFootballPredictionEnum.TU_5_0,
                BetFootballPredictionEnum.TU_5_5,
            ),
            cls.EXPRESS: (
                BetFootballPredictionEnum.EXPRESS,
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
    OFFICIAL = 'Офіційний'
    FRIENDLY = 'Товариський'
    UNKNOWN = '-'

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
    CLUB = 'Клуб'
    NATIONAL = 'Збірна'
    UNKNOWN = '-'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res


class CompetitionFootballCategoryEnum(StrEnum):
    CLUB = 'Клубний'
    NATIONAL = 'Збірний'
    UNKNOWN = '-'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res


BET_BASE_TABLE_FIELD_NAMES = {
    'date_game': 'Дата',
    'betting_service': 'Сервіс',
    'amount': 'Сума',
    'coefficient': 'Коеф.',
    'result': 'Результат',
    'profit': '+/-',
    'sport_kind__name': 'Спорт',
    'live_type': 'Тип',
    'is_favourite': '⭐',
    'action_delete': '☒',
}

BET_FOOTBALL_FIELDS_NAMES = {
    'date_game': 'Дата',
    'betting_service': 'Сервіс',
    'prediction': 'Прогноз',
    'amount': 'Сума',
    'coefficient': 'Коеф.',
    'result': 'Результат',
    'profit': '+/-',
    'competition': 'Турнір',
    'team_home': 'Ком. 1',
    'team_guest': 'Ком. 2',
    'live_type': 'Тип',
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
    '#5c5c5c',  # count line - grey
    '#236995',
]

OTHER_COLORS = [
    '#5c5c5c',   # count line - grey
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
    ('amount', 'Сума ставки'),
    ('coefficient', 'Коефіцієнт'),
    ('result', 'Результат ставки'),
    ('profit', 'Профіт'),
    ('sport_kind__name', 'Вид спорту'),
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


COMPETITION_RATING_TABLE_FIELD_NAMES = {
    'competition__name': 'Ліга',
    'count': 'К-сть',
    'profit_avg': 'Прибуток за ставку',
    'profit_sum': 'Загальний Прибуток',
    'roi': 'Рентабельність',
}


SPORT_KIND_RATING_TABLE_FIELD_NAMES = {
    'sport_kind__name': 'Спорт',
    'count': 'К-сть',
    'profit_avg': 'Прибуток за ставку',
    'profit_sum': 'Загальний Прибуток',
    'roi': 'Рентабельність',
}


BET_TYPE_RATING_TABLE_FIELD_NAMES = {
    'bet_type': 'Прогноз',
    'count': 'К-сть',
    'profit_avg': 'Прибуток за ставку',
    'profit_sum': 'Загальний Прибуток',
    'roi': 'Рентабельність',
}


MENU_TREE = {
    'bet_calendar': ['dashboard'],
    'bet_statistic': ['dashboard'],
    'bet_ratings': ['dashboard'],

    'bet_list': ['list'],
    'bet_football_list': ['list'],
    'bet_create': ['list', 'add_bet'],
    'bet_football_create': ['list', 'add_bet'],

    'bet_graphs_profit': ['graphs'],
    'bet_graphs_roi': ['graphs'],
    'bet_graphs_result': ['graphs'],
    'bet_graphs_amount': ['graphs'],
}


class ChartType(StrEnum):
    LINE = 'LINE'
    BAR = 'BAR'
