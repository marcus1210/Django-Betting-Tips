from django.apps import AppConfig
from material.frontend.apps import ModuleMixin



class BetsConfig(ModuleMixin, AppConfig):
    name = 'bets'
    icon = '<i class="material-icons">flight_takeoff</i>'
