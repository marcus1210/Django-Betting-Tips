from django.db import models


class Competition(models.Model):
    name = models.CharField(max_length = 255)
    country = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length = 255)
    country = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name='away_team')
    datetime_match = models.DateTimeField(null=True)
    completed = models.BooleanField(default = False)
    competition = models.ForeignKey(Competition, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "matches"

    def __str__(self):
        return '%s vs %s - %s' % (self.home_team, self.away_team, self.datetime_match.strftime('%d.%m.%Y'))


class MatchResult(models.Model):
    match = models.OneToOneField(Match, on_delete = models.CASCADE, null = True)
    home_scored = models.IntegerField()
    away_scored = models.IntegerField()
    extra_time = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s vs %s - %s - score: %s - %s   %s' % (self.match.home_team, self.match.away_team,
                                                   self.match.datetime_match.strftime('%d.%m.%Y'),
                                                   self.home_scored, self.away_scored, (lambda x: "ET" if x == True else "")(self.extra_time))


class OpenBet(models.Model):
    match = models.ForeignKey(Match, on_delete = models.CASCADE)
    BET_CHOICES = [('home_win', 'home_win'),
                   ('away_win', 'away_win'),
                   ('draw', 'draw')
                   ]
    bet = models.CharField(max_length = 10, choices = BET_CHOICES, default = 'none')
    dec_odds = models.FloatField()
    datetime_bet = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    website = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return '%s - %s - %s' % (self.match, self.bet, self.dec_odds)


class ClosedBet(models.Model):
    open_bet = models.OneToOneField(OpenBet, on_delete = models.CASCADE)
    OUTCOME_CHOICES = [('won', 'won'),
                       ('lost', 'lost')
                        ]
    outcome = models.CharField(max_length = 10, choices = OUTCOME_CHOICES, default = 'none')
    created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return '%s - %s' % (self.open_bet, self.outcome)






