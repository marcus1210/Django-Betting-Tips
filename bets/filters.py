import django_filters
from .models import Match, Competition

class MatchFilter(django_filters.FilterSet):
    #competition = django_filters.CharFilter()
    class Meta:
        model = Match
        fields = ['competition', 'datetime_match']
