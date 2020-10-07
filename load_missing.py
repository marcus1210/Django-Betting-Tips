import sys
import os
import django
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware
from django.conf import settings
import pytz, json


sys.path.append('C:\\Users\\Mark\\betting_tips')
os.environ['DJANGO_SETTINGS_MODULE'] = 'betting_tips.settings'
django.setup()

from bets.models import Match, MatchResult, Team, Competition, OpenBet, ClosedBet
            
#timezone = pytz.timezone('Europe/Ljubljana')
#for m in Match.objects.all():
#    dt_m = m.datetime_match
#    m.datetime_match = timezone.localize(datetime(dt_m.year,dt_m.month,dt_m.day,dt_m.hour,dt_m.minute), is_dst=False)
#    m.save(update_fields = ['datetime_match'])





#def get_outcome(home_scored, away_scored, bet):
#        outcome = 'lost'
#        if bet == 'home_win' and home_scored > away_scored:
#            outcome = 'won'
#        elif bet == 'away_win' and home_scored < away_scored:
#            outcome = 'won'
#        elif bet == 'draw' and home_scored == away_scored:
#            outcome = 'won'
#        return outcome
#           
#            
#            
#for ob in OpenBet.objects.all():
#        try:
#            cb = ClosedBet.objects.get(pk = ob.pk)
#        except:
#            match_result = MatchResult.objects.get(pk = ob.match.pk)
#            outcome = get_outcome(match_result.home_scored, match_result.away_scored, ob.bet)
#            ClosedBet.objects.create(pk = ob.pk, open_bet = ob, outcome = outcome)

            
#
#for match in Match.objects.all():
#    ht = match.home_team
#    at = match.away_team
#    dt = match.datetime_match
#    if len(Match.objects.filter(home_team = ht, away_team = at, datetime_match = dt)) > 1:
#        print(match, match.pk)
            
#
#unique_teams = {}
#teams_to_delete = []
#teams_with_no_country = []
#
#for team in Team.objects.all():
#    all_teams_with_this_name = Team.objects.filter(name = team.name)
#    if len(all_teams_with_this_name) > 1:
#        real_team_pk = []
#        for el in all_teams_with_this_name:
#            if el.country not in ["World", "Europe", "Africa", "South America"]:
#                real_team_pk.append(el.pk)
#            else:
#                teams_to_delete.append(team.pk)
#        if len(real_team_pk) == 1:
#            unique_teams[team.pk] = real_team_pk[0]
#        elif len(real_team_pk) == 0:
#            teams_with_no_country.append(team.pk)
#        else:
#            if real_team
#            print("More than 1 country", Team.objects.get(pk = real_team_pk[0]).name,Team.objects.get(pk = real_team_pk[0]).country,Team.objects.get(pk = real_team_pk[1]).name,Team.objects.get(pk = real_team_pk[1]).country)
#                
#        
#    else:
#        unique_teams[team.pk] = team.pk
        
        
