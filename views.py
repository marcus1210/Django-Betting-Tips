from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView
from .models import OpenBet, Match
from .filters import MatchFilter
from django_filters.views import FilterView
from . import helper_f



class AboutView(TemplateView):
    template_name = 'bets/about.html'


class MatchListView(FilterView):
    model = Match
    template_name = 'bets/matches_list.html'
    filterset_class = MatchFilter

    def get_queryset(self):
        context = Match.objects.filter(completed = False)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matches_with_openBets = []
        for match in context['object_list']:
            openBets = OpenBet.objects.filter(match = match)
            match_name = '%s - %s' % (match.home_team, match.away_team)
            match_dt = helper_f.date_format(match.datetime_match)
            match_competition = match.competition.country + " - " + match.competition.name
            if len(openBets) == 3:
                openBets_info = []
                betting_odds_dict = {}
                for ob in openBets:
                    openBets_info.append([ob.bet, helper_f.bet_format(ob.bet), str(ob.dec_odds)])
                    betting_odds_dict[ob.bet] = ob.dec_odds

                openBets_info = sorted(openBets_info)
                openBets_info.reverse()
                implied_probs = helper_f.shin_probs(betting_odds_dict)
                for ob in openBets_info:
                    ob.append(implied_probs[ob[0]])



                matches_with_openBets.append((match_name, match_dt, match_competition, openBets_info, match.pk))

        context['matches_with_openBets'] = matches_with_openBets
        return context




class MatchListView22(ListView):
    model = Match
    template_name = 'bets/matches_list.html'

    # def get_queryset(self):
    #     competition = self.request.GET.get('competition', 'DFB Pokal')
    #     country = self.request.GET.get('country', 'Germany')
    #     new_context = Match.objects.filter(competition__name = competition, competition__country = country)
    #     return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matches_with_openBets = []
        for match in Match.objects.filter(completed = False):
            openBets = OpenBet.objects.filter(match = match)
            match_name = '%s - %s' % (match.home_team, match.away_team)
            match_dt = helper_f.date_format(match.datetime_match)
            match_competition = match.competition.country + " - " + match.competition.name
            if len(openBets) == 3:
                openBets_info = []
                betting_odds_dict = {}
                for ob in openBets:
                    openBets_info.append([ob.bet, helper_f.bet_format(ob.bet), str(ob.dec_odds)])
                    betting_odds_dict[ob.bet] = ob.dec_odds

                openBets_info = sorted(openBets_info)
                openBets_info.reverse()
                implied_probs = helper_f.shin_probs(betting_odds_dict)
                for ob in openBets_info:
                    ob.append(implied_probs[ob[0]])



                matches_with_openBets.append((match_name, match_dt, match_competition, openBets_info, match.pk))

        context['matches_with_openBets'] = matches_with_openBets
        #context['competition'] = self.request.GET.get('competition', 'DFB Pokal')
        #context['country'] = self.request.GET.get('country', 'Germany')
        return context



class MatchDetailView(DetailView):
    model = Match
    template_name = 'bets/matches_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = Match.objects.get(pk = self.kwargs['pk'])
        openBets = OpenBet.objects.filter(match = match)
        match_name = '%s - %s' % (match.home_team, match.away_team)
        match_dt = helper_f.date_format(match.datetime_match)
        match_competition = match.competition.country + " - " + match.competition.name
        if len(openBets) == 3:
            openBets_info = []
            betting_odds_dict = {}
            for ob in openBets:
                openBets_info.append([ob.bet, helper_f.bet_format(ob.bet), str(ob.dec_odds)])
                betting_odds_dict[ob.bet] = ob.dec_odds

            openBets_info = sorted(openBets_info)
            openBets_info.reverse()
            implied_probs = helper_f.shin_probs(betting_odds_dict)
            hist_probs = helper_f.hist_probs(betting_odds_dict)
            for ob in openBets_info:
                ob.append(implied_probs[ob[0]])
                ob.append(hist_probs[ob[0]])

            match_with_openBets = [match_name, match_dt, match_competition, openBets_info, match.pk, hist_probs]

        context["match_with_openBets"] = match_with_openBets
        return context







