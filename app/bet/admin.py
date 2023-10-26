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
    list_display = ['get_user_username', 'bet', 'amount', 'coefficient', 'profit', 'result', 'date_game']

    @admin.display(ordering='user__username', description='User')
    def get_user_username(self, obj):
        return obj.user.username


class BetFootballAdmin(admin.ModelAdmin):
    list_display = ['get_user_username', 'bet', 'amount', 'coefficient', 'result',
                    'team_home', 'team_guest', 'bet_type',
                    'competition', 'game_status', 'is_home_guest']

    @admin.display(ordering='user__username', description='User')
    def get_user_username(self, obj):
        return obj.user.username


admin.site.register(Country, CountryAdmin)
admin.site.register(SportKind, SportKindAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(CompetitionBase, CompetitionBaseAdmin)
admin.site.register(CompetitionFootball, CompetitionFootballAdmin)
admin.site.register(BetBase, BetBaseAdmin)
admin.site.register(BetFootball, BetFootballAdmin)
