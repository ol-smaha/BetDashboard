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


class BetVariant(StrEnum):
    EXPRESS = 'Експрес'
    W1 = 'П1'
    X = 'Нічия'
    W2 = 'П2'
    WX1 = '1-Х'
    NOT_X = '1-2'
    WX2 = '2-Х'
    O_Z = 'ОЗ'
    TO_0_5 = 'ТБ 0.5'
    TU_0_5 = 'ТМ 0.5'
    TO_1_0 = 'ТБ 1.0'
    TU_1_0 = 'ТМ 1.0'
    TO_1_5 = 'ТБ 1.5'
    TU_1_5 = 'ТМ 1.5'
    TO_2_0 = 'ТБ 2.0'
    TU_2_0 = 'ТМ 2.0'
    TO_2_5 = 'ТБ 2.5'
    TU_2_5 = 'ТМ 2.5'
    TO_3_0 = 'ТБ 3.0'
    TU_3_0 = 'ТМ 3.0'
    TO_3_5 = 'ТБ 3.5'
    TU_3_5 = 'ТМ 3.5'
    TO_4_0 = 'ТБ 4.0'
    TU_4_0 = 'ТМ 4.0'
    TO_4_5 = 'ТБ 4.5'
    TU_4_5 = 'ТМ 4.5'
    TO_5_0 = 'ТБ 5.0'
    TU_5_0 = 'ТМ 5.0'
    TO_5_5 = 'ТБ 5.5'
    TU_5_5 = 'ТМ 5.5'
    F1_0_0 = 'Ф1 (0)'
    F2_0_0 = 'Ф1 (0)'
    F1_PLUS_0_5 = 'Ф1 (+0.5)'
    F2_PLUS_0_5 = 'Ф2 (+0.5)'
    F1_PLUS_1_0 = 'Ф1 (+1.0)'
    F2_PLUS_1_0 = 'Ф2 (+1.0)'
    F1_PLUS_1_5 = 'Ф1 (+1.5)'
    F2_PLUS_1_5 = 'Ф2 (+1.5)'
    F1_PLUS_2_0 = 'Ф1 (+2.0)'
    F2_PLUS_2_0 = 'Ф2 (+2.0)'
    F1_PLUS_2_5 = 'Ф1 (+2.5)'
    F2_PLUS_2_5 = 'Ф2 (+2.5)'
    F1_PLUS_3_0 = 'Ф1 (+3.0)'
    F2_PLUS_3_0 = 'Ф2 (+3.0)'
    F1_MINUS_0_5 = 'Ф1 (-0.5)'
    F2_MINUS_0_5 = 'Ф2 (-0.5)'
    F1_MINUS_1_0 = 'Ф1 (-1.0)'
    F2_MINUS_1_0 = 'Ф2 (-1.0)'
    F1_MINUS_1_5 = 'Ф1 (-1.5)'
    F2_MINUS_1_5 = 'Ф2 (-1.5)'
    F1_MINUS_2_0 = 'Ф1 (-2.0)'
    F2_MINUS_2_0 = 'Ф2 (-2.0)'
    F1_MINUS_2_5 = 'Ф1 (-2.5)'
    F2_MINUS_2_5 = 'Ф2 (-2.5)'
    F1_MINUS_3_0 = 'Ф1 (-3.0)'
    F2_MINUS_3_0 = 'Ф2 (-3.0)'

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
    WDL = '1-X-2'
    WX = '1X-12-2X/'
    FORA = 'Fora'
    TOTAL = 'Total '
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res


class GameStatusEnum(StrEnum):
    OFFICIAL = 'OFFICIAL'
    FRIENDLY = 'FRIENDLY'
    UNKNOWN = 'UNKNOWN'

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
    'date_game': 'Date Of Game',
    'bet': 'Bet',
    'amount': 'Amount',
    'coefficient': 'Coefficient',
    'result': 'Bet Result',
    'profit': 'Profit',
    'sport_kind': 'Kind Of Sport',
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

BET_BASE_ORDERING_FIELDS_CHOICES = (
    ('date_game', 'Дата події'),
    ('bet', 'Прогноз'),
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