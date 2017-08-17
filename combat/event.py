from enum import Enum
from typing import Callable, List, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from Pokemon import Pokemon

class EventType(Enum):
    STATUS_AFFECTS_POKEMON = "statusaffectpokemon"
    STATUS_INFLICT_CHANCE = "statusinflictchance"
    STATUS_INFLICTED = "statusinflicted"
    POKEMON_ATTACKS = "pokemonattacks"
    RECOIL_DAMAGE = "recoildamage"
    ABSORB_HEALTH = "absorbhealth"
    STATUS_REMOVE = "statusremove"
    TURN_END = "turnend"
    POKEMON_MISSES = "pokemonmisses"


class EventData:
    def __init__(self, function: Callable[["EventData"], List["Event"]], field=None,
                 defender: "Pokemon"=None, attacker: "Pokemon"=None, damage=0, chance: float=None):
        """
        Function is a function which, when called, executes the event
        :param function:
        :param field:
        :param defender:
        :param attacker:
        :param damage:
        :param chance:
        """
        self.__field = field
        self.__defendant = defender
        self.__attacker = attacker
        self.__def_damage = damage
        self.__chance = chance
        self.__call = function

    def call(self):
        return self.__call(self)

    @property
    def field(self):
        return self.__field

    @property
    def defender(self):
        return self.__defendant

    @property
    def attacker(self):
        return self.__attacker

    @property
    def damage(self):
        return self.__def_damage

    @property
    def chance(self):
        return self.__chance


class Event:
    def __init__(self, event_type: EventType, data_object: EventData):
        self.__type = event_type
        self.__data = data_object

    def call(self):
        return self.__data.call()

    @property
    def type(self):
        return self.__type

