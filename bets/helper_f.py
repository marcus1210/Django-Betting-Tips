from datetime import datetime
import shin
from .models import OpenBet, Match

MONTHS = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

BET_TRANSFORM = {
    "home_win": "1", "draw": "X", "away_win": "2"
}


def date_format(date):
    return str(date.day) + " " + MONTHS[date.month] + " " + str(date.year) +\
            " " + str(date.hour) + ":" + str(date.minute) + " CET"

def bet_format(bet):
    return BET_TRANSFORM[bet]




# This function returns Shin probabilities, which are more accurate than inversed odds
def shin_probs(betting_odds_dict):
    all_dec_odds = [betting_odds_dict['home_win'], betting_odds_dict['draw'], betting_odds_dict['away_win']]
    implied_probabilities = shin.calculate_implied_probabilities(all_dec_odds)['implied_probabilities']
    probs = {}
    prob_hw = round(100 * implied_probabilities[0], 2)
    prob_d = round(100 * implied_probabilities[1], 2)
    prob_aw = round(100 * implied_probabilities[2], 2)
    if prob_d + prob_hw + prob_aw > 100:
        prob_aw -= 0.01
    elif prob_d + prob_hw + prob_aw < 100:
        prob_aw += 0.01
    probs['home_win'] = str(prob_hw) + " %"
    probs['draw'] = str(prob_d) + " %"
    probs['away_win'] = str(prob_aw) + " %"
    return probs


def hist_probs2(betting_odds_dict):
    rel1 = OpenBet.objects.filter(is_active=False, dec_odds__range=(
    betting_odds_dict["away_win"] * 0.9, betting_odds_dict["away_win"] * 1.1), bet="away_win").select_related('match')
    rel2 = OpenBet.objects.filter(is_active=False, dec_odds__range=(
    betting_odds_dict["home_win"] * 0.9, betting_odds_dict["home_win"] * 1.1), bet="home_win").select_related('match')
    rel3 = OpenBet.objects.filter(is_active=False,
                                  dec_odds__range=(betting_odds_dict["draw"] * 0.9, betting_odds_dict["draw"] * 1.1),
                                  bet="draw").select_related('match')

    all_matches1 = []
    for el in rel1:
        all_matches1.append(el.match.pk)

    all_matches2 = []
    for el in rel2:
        all_matches2.append(el.match.pk)

    all_matches3 = []
    for el in rel3:
        all_matches3.append(el.match.pk)

    all_matches = set(all_matches1) & set(all_matches2) & set(all_matches3)
    relevant_bets = OpenBet.objects.filter(match__pk__in = all_matches).select_related('closedbet')
    probs = {
        "home_win": 0,
        "draw": 0,
        "away_win": 0
    }
    for el in relevant_bets:
        if el.closedbet.outcome == "won":
            probs[el.bet] += 1
    probs["home_win"] = str(round(100 * probs["home_win"] / max(1,len(all_matches)), 2)) + " %"
    probs["draw"] = str(round(100 * probs["draw"] / max(1,len(all_matches)), 2)) + " %"
    probs["away_win"] = str(round(100 * probs["away_win"] / max(1,len(all_matches)), 2)) + " %"
    return probs




def hist_probs(betting_odds_dict):
    probs = {}
    for bet, dec_odds in betting_odds_dict.items():
        relevant_bets = OpenBet.objects.filter(is_active = False).select_related('closedbet').filter(bet=bet, dec_odds=dec_odds)
        won = 0
        for el in relevant_bets:
            if el.closedbet.outcome == "won":
                won += 1
        probs[bet] = str(round(100 * won / len(relevant_bets), 2)) + " %"

    return probs