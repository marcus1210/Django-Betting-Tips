from django.urls import path
from .views import AboutView, MatchListView, MatchDetailView

urlpatterns = [
    path('matches/', MatchListView.as_view(), name = "matches_list"),
    path('matches/<int:pk>/', MatchDetailView.as_view(), name = 'matches_detail'),
    path('about/', AboutView.as_view(), name="about"),

]