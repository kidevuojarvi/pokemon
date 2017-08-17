from enum import Enum
from typing import Any, Callable


class EventType(Enum):
    STATUS_AFFECTS_POKEMON = "statusaffectpokemon"
    STATUS_INFLICTED = "statusinflicted"
    POKEMON_ATTACKS = "pokemonattacks"
    RECOIL_DAMAGE = "recoildamage"
    ABSORB_HEALTH = "absorbhealth"
    STATUS_REMOVE = "statusremove"
    TURN_END = "turnend"


class EventData:
    def __init__(self, field=None, defendant=None, attacker=None, defender_damage=0, attacker_damage=0,
                 function=Callable):
        self.__field = field
        self.__defendant = defendant
        self.__attacker = attacker
        self.__def_damage = defender_damage
        self.__att_damage = attacker_damage,
        self.__function_call = function


class Event:
    # TODO: Specify data object better. Maybe have it have default
    # Nones and each event fills out the data they need
    def __init__(self, event_type: EventType, data_object: EventData):
        self.__type = event_type

    @property
    def type(self):
        return self.__type

