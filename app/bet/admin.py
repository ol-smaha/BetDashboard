from django.contrib import admin

from bet.models import Country, SportKind, Team, CompetitionBase, CompetitionFootball, BetBase, BetFootball


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code2', 'code3']


class SportKindAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'country']


class CompetitionBaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'sport_kind', 'country']


class CompetitionFootballAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sport_kind', 'country']


class BetBaseAdmin(admin.ModelAdmin):
    list_display = ['bet', 'amount', 'coefficient', 'result']


class BetFootballAdmin(admin.ModelAdmin):
    list_display = ['bet', 'amount', 'coefficient', 'result',
                    'team_home', 'team_guest', 'bet_type',
                    'competition', 'game_status', 'is_home_guest']


admin.site.register(Country, CountryAdmin)
admin.site.register(SportKind, SportKindAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(CompetitionBase, CompetitionBaseAdmin)
admin.site.register(CompetitionFootball, CompetitionFootballAdmin)
admin.site.register(BetBase, BetBaseAdmin)
admin.site.register(BetFootball, BetFootballAdmin)
