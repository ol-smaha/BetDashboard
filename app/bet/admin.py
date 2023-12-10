from django.contrib import admin

from bet.models import Country, SportKind, Team, CompetitionBase, BetBase, BetFootball, \
    BettingService
from bet.utils import generate_bets, generate_football_bets, generate_default_data


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code2', 'code3']


class SportKindAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sport_kind', 'country']


class CompetitionBaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'sport_kind', 'country']
    actions = ["create_from_csv"]

    @admin.action(description="Generate competitions and teams from csv")
    def create_from_csv(self, request, queryset):
        generate_default_data()


class BetBaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'coefficient', 'profit', 'result', 'live_type',
                    'date_game', 'sport_kind', 'is_favourite']
    actions = ["generate_bet_base", "trigger_save"]

    @admin.action(description="Generate Bets")
    def generate_bet_base(self, request, queryset):
        generate_bets()

    @admin.action(description="Trigger Save Method")
    def trigger_save(self, request, queryset):
        for obj in queryset:
            obj.save()


class BetFootballAdmin(admin.ModelAdmin):
    list_display = ['user', 'prediction', 'amount', 'coefficient', 'result',
                    'team_home', 'team_guest', 'bet_type',
                    'competition', 'game_status']
    actions = ["generate_bet_football", "trigger_save"]

    @admin.action(description="Generate Football Bets")
    def generate_bet_football(self, request, queryset):
        generate_football_bets()

    @admin.action(description="Trigger Save Method")
    def trigger_save(self, request, queryset):
        for obj in queryset:
            obj.save()


class BettingServiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']


admin.site.register(Country, CountryAdmin)
admin.site.register(SportKind, SportKindAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(CompetitionBase, CompetitionBaseAdmin)
admin.site.register(BetBase, BetBaseAdmin)
admin.site.register(BetFootball, BetFootballAdmin)
admin.site.register(BettingService, BettingServiceAdmin)

