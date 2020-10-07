from django.contrib import admin
from .models import OpenBet, ClosedBet, Match, MatchResult, Team, Competition


@admin.register(OpenBet)
class OpenBetAdmin(admin.ModelAdmin):
    list_display = ['match','bet', 'dec_odds', 'datetime_bet', 'is_active', 'created', 'datetime_match']
    list_filter = ['match', 'bet', 'datetime_bet','is_active','dec_odds']

    def datetime_match(self, obj):
        return Match.objects.get(id = obj.match.id).datetime_match

    datetime_match.admin_order_field = 'match__datetime_match'



@admin.register(ClosedBet)
class ClosedBetAdmin(admin.ModelAdmin):
    list_display = ['match_result','bet', 'outcome', 'created']
    list_filter = ['outcome']

    def match_result(self, obj):
        return MatchResult.objects.get(match = obj.open_bet.match)

    def bet(self, obj):
        return obj.open_bet.bet


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['datetime_match', 'competition','home_team','away_team', 'completed', 'created']
    list_filter = ['datetime_match', 'competition','home_team','away_team', 'completed']

@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ['match','home_scored','away_scored', 'created']
    list_filter = ['match','home_scored','away_scored']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name','country', 'created']
    list_filter = ['name','country']

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['name','country', 'created']
    list_filter = ['name','country']

