import sys, os, csv
import pandas as pd
import numpy as np
import shin
import django
from django.conf import settings
sys.path.append('C:\\Users\\Mark\\betting_tips')
os.environ['DJANGO_SETTINGS_MODULE'] = 'betting_tips.settings'
django.setup()


from bets.models import Match, MatchResult, Team, Competition, OpenBet, ClosedBet

# This function returns inverse normalized probabilities
def inverse_probs(betting_odds):
    booksum = sum(1 / np.array(list(betting_odds.values())))
    probs = {}
    for bet, dec_odds in betting_odds.items():
        probs[bet] = 1 / dec_odds / booksum
    return probs

# This function returns Shin probabilities, which are more accurate than inversed odds
def shin_probs(betting_odds):
    all_dec_odds = [betting_odds['home_win'], betting_odds['draw'], betting_odds['away_win']]
    implied_probabilities = shin.calculate_implied_probabilities(all_dec_odds)['implied_probabilities']
    probs = {}
    probs['home_win'] = implied_probabilities[0]
    probs['draw'] = implied_probabilities[1]
    probs['away_win'] = implied_probabilities[2]
    return probs
    

#
#booksums = {}
#
#for match in Match.objects.all():
#    bets = OpenBet.objects.filter(match = match)
#    if len(bets) != 3:
#        print(match, len(bets))
#    elif len(bets) == 3:
#        booksum = 0
#        for bet in bets:
#            booksum += 1/bet.dec_odds
#        try:
#            booksums[match.competition.name + match.competition.country] += [booksum]
#        except:
#            booksums[match.competition.name + match.competition.country] = [booksum]
#        if booksum < 1:
#            for bet in bets:
#                print(bet.dec_odds, match)
#
#
#
#
#booksums_ordered = {}
#for k,v in booksums.items():
#    booksums_ordered[k] = sum(v)/len(v)
#
#booksums_ordered = pd.Series(booksums_ordered)
#booksums_ordered = booksums_ordered.sort_values()
#
#for i in range(len(booksums_ordered)):
#    print(booksums_ordered.index[i], booksums_ordered.iloc[i])
    

# This function returns the historical probability of a bet = ("home_win", "away_win","draw") with the given dec_odds
#def hist_prob(bet, dec_odds):
bet = "home_win"
dec_odds = 1.31
relevant_bets = OpenBet.objects.select_related('closedbet').filter(bet = bet, dec_odds = dec_odds)

won = 0
for el in relevant_bets:
    if el.closedbet.outcome == "won":
        won += 1

print(won, len(relevant_bets),won / len(relevant_bets))


betting_odds_dict = {"home_win": 25.41, "draw": 10.93, "away_win": 1.07}

rel1 = OpenBet.objects.filter(is_active = False, dec_odds__range = (betting_odds_dict["away_win"]*0.9,betting_odds_dict["away_win"]*1.1), bet = "away_win")
rel2 = OpenBet.objects.filter(is_active = False, dec_odds__range = (betting_odds_dict["home_win"]*0.9,betting_odds_dict["home_win"]*1.1), bet = "home_win")
rel3 = OpenBet.objects.filter(is_active = False, dec_odds__range = (betting_odds_dict["draw")]*0.9,betting_odds_dict["draw")]*1.1), bet = "draw")

all_matches = []
for el in rel:
      all_matches.append(el.match.pk)


