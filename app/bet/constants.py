from enum import StrEnum


class BetResultEnum(StrEnum):
    WIN = 'WIN'
    DRAWN = 'DRAWN'
    LOSE = 'LOSE'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def choices(cls):
        res = (
            (cls.WIN, cls.WIN),
            (cls.DRAWN, cls.DRAWN),
            (cls.LOSE, cls.LOSE),
            (cls.UNKNOWN, cls.UNKNOWN),
        )
        return res

    @classmethod
    def values(cls):
        res = [cls.WIN, cls.DRAWN, cls.LOSE, cls.UNKNOWN]
        return res


class BetTypeEnum(StrEnum):
    WDL = '1-X-2'
    WX = '1X-12-2X/'
    FORA = 'Fora'
    TOTAL = 'Total '
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def choices(cls):
        res = (
            (cls.WDL, cls.WDL),
            (cls.WX, cls.WX),
            (cls.FORA, cls.FORA),
            (cls.TOTAL, cls.TOTAL),
            (cls.UNKNOWN, cls.UNKNOWN),
        )
        return res


class GameStatusEnum(StrEnum):
    OFFICIAL = 'OFFICIAL'
    FRIENDLY = 'FRIENDLY'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def choices(cls):
        res = (
            (cls.OFFICIAL, cls.OFFICIAL),
            (cls.FRIENDLY, cls.FRIENDLY),
            (cls.UNKNOWN, cls.UNKNOWN),
        )
        return res


class TeamCategoryEnum(StrEnum):
    CLUB = 'CLUB'
    NATIONAL = 'NATIONAL'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def choices(cls):
        res = (
            (cls.CLUB, cls.CLUB),
            (cls.NATIONAL, cls.NATIONAL),
            (cls.UNKNOWN, cls.UNKNOWN),
        )
        return res


class CompetitionFootballCategoryEnum(StrEnum):
    CLUB = 'CLUB'
    NATIONAL = 'NATIONAL'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def choices(cls):
        res = (
            (cls.CLUB, cls.CLUB),
            (cls.NATIONAL, cls.NATIONAL),
            (cls.UNKNOWN, cls.UNKNOWN),
        )
        return res


BET_BASE_TABLE_FIELD_NAMES = {
    'date_game': 'Date Of Game',
    'bet': 'Bet',
    'amount': 'Amount',
    'coefficient': 'Coefficient',
    'result': 'Bet Result',
    'sport_kind': 'Kind Of Sport',
    'date_betting': 'Date Of Bet',
}


DEFAULT_MORRIS_CHART_COLORS = [
    '#5969ff',
    '#ff407b',
]
