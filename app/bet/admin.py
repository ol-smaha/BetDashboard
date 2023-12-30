from django.contrib import admin

from bet.models import Country, SportKind, Team, CompetitionBase, BetBase, BetFootball, \
    BettingService
from users.models import UnregisteredContact
from bet.utils import generate_bets, generate_football_bets, user_data_setup, create_default_countries


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'flag_code']

    actions = ["generate_countries"]

    @admin.action(description="Generate countries")
    def generate_countries(self, request, queryset):
        create_default_countries()


class SportKindAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']
    list_filter = ["user"]


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_extended', 'category', 'sport_kind', 'country']


class CompetitionBaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'name_extended', 'sport_kind', 'country']
    list_filter = ["user"]
    actions = ["user_data_setup"]

    @admin.action(description="Generate competitions and teams from csv")
    def create_from_csv(self, request, queryset):
        user_data_setup(request.user)


class BetBaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'coefficient', 'profit', 'result', 'is_live_type',
                    'date_game', 'sport_kind', 'is_favourite']
    list_filter = ["user", 'result']
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
    list_filter = ["user"]
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
    list_filter = ["user"]


class UnregisteredContactAdmin(admin.ModelAdmin):
    list_display = ['unregistered_email', 'message']
    list_filter = ["unregistered_email"]


admin.site.register(Country, CountryAdmin)
admin.site.register(SportKind, SportKindAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(CompetitionBase, CompetitionBaseAdmin)
admin.site.register(BetBase, BetBaseAdmin)
admin.site.register(BetFootball, BetFootballAdmin)
admin.site.register(BettingService, BettingServiceAdmin)
admin.site.register(UnregisteredContact, UnregisteredContactAdmin)

