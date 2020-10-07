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

### To delete all:

#from bets.models import Match, MatchResult, Team, Competition, OpenBet, ClosedBet



### DATAFLOW: every x hours, the result of scraping (two csv files) are loaded onto this script.
# From the first CSV file(open_bets_csv) the Teams and Competitions are updated in case there is a new
# team or competition. Then the Match model/table is updated in case a match(uniquely defined as 
# home_team, away_team, datetime_match) has never been seen in previous versions of open_bets_csv.
# After that the OpenBet model is updated. Each row is defined uniquely by match 
# bet, dec_odds, website. If there is no such instance in the table we add the row, because it is either 
# the first time this match was open to betting or the odds changed since the last version of the scraped file.


from bets.models import Team, Competition, MatchResult, Match, OpenBet, ClosedBet

def to_datetime_f(s):
    return pd.to_datetime(s, dayfirst = True)


def update_teams(open_bets_csv):
    for i in range(len(open_bets_csv)):
        home_team_name = open_bets_csv.iloc[i]["home_team"]
        away_team_name = open_bets_csv.iloc[i]["away_team"]
        home_team_country = open_bets_csv.iloc[i]["country_home_team"]
        away_team_country = open_bets_csv.iloc[i]["country_away_team"]
        all_teams_in_database = list(Team.objects.all().values_list('name', flat = True))
        if home_team_name not in all_teams_in_database:
            Team.objects.create(name = home_team_name, country = home_team_country)
        if away_team_name not in all_teams_in_database:
            Team.objects.create(name = away_team_name, country = away_team_country)
            



def update_competitions(open_bets_csv):
    for i in range(len(open_bets_csv)):
        competition_name = open_bets_csv.iloc[i]["competition"]
        home_team_country = open_bets_csv.iloc[i]["country_home_team"]
        away_team_country = open_bets_csv.iloc[i]["country_away_team"]
        if home_team_country != away_team_country:
            competition_country = 'Europe'
        else:
            competition_country = home_team_country
        all_competitions_in_database = list(Competition.objects.all().values_list('name', flat=True))
        if competition_name not in all_competitions_in_database:
            Competition.objects.create(name = competition_name, country = competition_country)
       



def update_matches(open_bets_csv):
    for i in range(len(open_bets_csv)):
        home_team_name = open_bets_csv.iloc[i]["home_team"]
        away_team_name = open_bets_csv.iloc[i]["away_team"]
        assert home_team_name != away_team_name , "Home Team and Away Team are the same!"
        competition_name = open_bets_csv.iloc[i]["competition"]
        # Some timezones are noneistent, so we just add an hour there
        try:
            datetime_match = make_aware(open_bets_csv.iloc[i]["datetime_match"])
        except:
            timezone = pytz.timezone('Europe/Ljubljana')
            datetime_match = timezone.localize(open_bets_csv.iloc[i]["datetime_match"], is_dst=False)

        if len(Match.objects.filter(home_team__name = home_team_name,
                                    away_team__name = away_team_name,
                                    datetime_match = datetime_match)) == 0:

            Match.objects.create(home_team = Team.objects.get(name = home_team_name),
                                 away_team = Team.objects.get(name = away_team_name),
                                 datetime_match = datetime_match,
                                 competition = Competition.objects.get(name = competition_name))
            





def update_open_bets(open_bets_csv):
    for i in range(len(open_bets_csv)):
        home_team_name = open_bets_csv.iloc[i]["home_team"]
        away_team_name = open_bets_csv.iloc[i]["away_team"]
        assert home_team_name != away_team_name , "Home Team and Away Team are the same!"
        competition_name = open_bets_csv.iloc[i]["competition"]
        try:
            datetime_match = make_aware(open_bets_csv.iloc[i]["datetime_match"])
        except:
            timezone = pytz.timezone('Europe/Ljubljana')
            datetime_match = timezone.localize(open_bets_csv.iloc[i]["datetime_match"], is_dst=False)
        dec_odds = open_bets_csv.iloc[i]["odds"]
        bet = open_bets_csv.iloc[i]["bet"]
        website = open_bets_csv.iloc[i]["website"]
        
        if len(OpenBet.objects.filter(match__home_team__name = home_team_name,
                                    match__away_team__name = away_team_name,
                                    match__datetime_match = datetime_match,
                                    bet = bet, 
                                    website = website, 
                                    dec_odds = dec_odds)) == 0:

            OpenBet.objects.create(match = Match.objects.get(home_team = Team.objects.get(name = home_team_name),
                                                             away_team = Team.objects.get(name = away_team_name),
                                                             datetime_match = datetime_match,
                                                             competition__name = competition_name),
                                    bet = bet,
                                    dec_odds = dec_odds,
                                    website = website)
                                   
            
            







def update_match_results(scores_csv):
    for match in Match.objects.filter(completed = False):
        for i in range(len(scores_csv)):
            home_team_name = scores_csv.iloc[i]["home_team"]
            away_team_name = scores_csv.iloc[i]["away_team"]
            home_team_scored = scores_csv.iloc[i]["home_scored"]
            away_team_scored = scores_csv.iloc[i]["away_scored"]
            extra_time = scores_csv.iloc[i]["extra_time"]
            try:
                datetime_match = make_aware(scores_csv.iloc[i]["datetime_match"])
            except:
                timezone = pytz.timezone('Europe/Ljubljana')
                datetime_match = timezone.localize(scores_csv.iloc[i]["datetime_match"], is_dst=False)
            if str(match.home_team) == home_team_name and str(match.away_team) == away_team_name \
            and (match.datetime_match.astimezone(pytz.timezone(settings.TIME_ZONE)) - datetime_match).days < 2\
            and match.completed == False:
                
                if extra_time == "yes":
                    MatchResult.objects.create(match = match, home_scored = home_team_scored, away_scored = away_team_scored, extra_time = True)
                else:
                    MatchResult.objects.create(match = match, home_scored = home_team_scored, away_scored = away_team_scored)
                match.completed = True
                match.save(update_fields = ['completed'])
                #scores_csv = scores_csv.drop([i])
                break

#        if (match.datetime_match.astimezone(pytz.timezone(settings.TIME_ZONE)) - make_aware(datetime.now())).days < 0:
#            print(match, 'is completed and result not in scores_csv')




def get_outcome(match_result, open_bet):
    if match_result.extra_time == False:
        outcome = 'lost'
        if open_bet.bet == 'home_win' and match_result.home_scored > match_result.away_scored:
            outcome = 'won'
        elif open_bet.bet == 'away_win' and match_result.home_scored < match_result.away_scored:
            outcome = 'won'
        elif open_bet.bet == 'draw' and match_result.home_scored == match_result.away_scored:
            outcome = 'won'
        return outcome
    else:
        date_range_start = match_result.match.datetime_match - relativedelta(months = 6)
        previous_matches = MatchResult.objects.filter(match__home_team = match_result.match.away_team,
                                                      match__away_team = match_result.match.home_team,
                                                      match__competition = match_result.match.competition,
                                                      match__datetime_match__range = [date_range_start, match_result.match.datetime_match]).exclude(\
                                                            match__competition__name = "World Cup").exclude(match__competition__name = "Euro").exclude(\
                                                            match__competition__name = "Copa Libertadores").exclude(match__competition__name = "Africa Cup of Nations").\
                                                              exclude(match__competition__name = "Club Friendly")
        
        #assert len(previous_matches) <= 1, "More than one match from the same competition in case of EXTRA TIME"
        if len(previous_matches) == 1: # There was a previous match and the result for our current instance of match_result was
            # a mirror result of that result from the previous match. 
            outcome = 'lost'
            if open_bet.bet == 'home_win' and previous_matches[0].home_scored > previous_matches[0].away_scored:
                outcome = 'won'
            elif open_bet.bet == 'away_win' and previous_matches[0].home_scored < previous_matches[0].away_scored:
                outcome = 'won'
            elif open_bet.bet == 'draw' and previous_matches[0].home_scored == previous_matches[0].away_scored:
                outcome = 'won'
            
        else: # No previous match - probably a final - outcome after full time is a draw. Or if too many, probably one match only
            outcome = "lost"
            if open_bet.bet == "draw":
                outcome = "won"
    
        return outcome        
        



def update_closed_bets():
    for open_bet in OpenBet.objects.filter(is_active = True):
        if open_bet.match.completed == True:
            match_result = MatchResult.objects.get(match = open_bet.match)
            outcome = get_outcome(match_result, open_bet)
            ClosedBet.objects.create(open_bet = open_bet, outcome = outcome)
            open_bet.is_active = False
            open_bet.save(update_fields = ['is_active'])


### UPLOAD
            
json_file = open("competitions.json")
countries_and_competitions = json.load(json_file)["country_competitions"]
json_file.close()

for country in list(countries_and_competitions.keys()):
    if country == "Canada":
        print(country)
        file_open_bets = "scrapers\\Historical Results 8.8.2020\\Open_bets_" + country + ".csv"
        file_scores = "scrapers\\Historical Results 8.8.2020\\Scores_" + country + ".csv"
        open_bets_csv = pd.read_csv(file_open_bets, converters = {"datetime_match": to_datetime_f, "datetime_scraped": to_datetime_f}).sort_values(by="datetime_match")
        scores_csv = pd.read_csv(file_scores, converters = {"datetime_match": to_datetime_f}).sort_values(by="datetime_match")

        update_teams(open_bets_csv)
        update_competitions(open_bets_csv)
        update_matches(open_bets_csv)
        update_open_bets(open_bets_csv)
        update_match_results(scores_csv)
        update_closed_bets()