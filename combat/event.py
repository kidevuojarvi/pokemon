from enum import Enum
from typing import Callable, List, TYPE_CHECKING, Any
import random

if TYPE_CHECKING:
    from Pokemon import Pokemon


class EventType(Enum):
    SLEEP_INFLICTING = "sleepinflicting"
    FINAL_SLEEP_INFLICTED = "sleepinflicted"
    PARALYZE_INFLICTING = "paralyzeinflicting"
    FINAL_PARALYZE_INFLICTED = "paralyzeinflicted"
    ATTACK_TRIES_TO_HIT = "pokemonattacks"
    FINAL_ATTACK_DID_DAMAGE = "attackhits"
    FINAL_ATTACK_CRIT = "attackcriticals"
    RECOIL_DAMAGE = "recoildamage"
    FINAL_TOOK_RECOIL_DAMAGE = "tookrecoil"
    ABSORB_HEALTH = "absorbhealth"
    FINAL_HEALTH_ABSORBED = "absorbedhealth"
    STATUS_REMOVE = "statusremove"
    TURN_END = "turnend"
    ATTACK_MISSES = "pokemonmisses"
    ATTACK_DOES_EXACT_DAMAGE = "attackexactdamage"
    ATTACK_FAILED = "attackfailed"
    MULTI_HIT_TIMES = "multihittimes"
    BURN_INFLICTING = "burninflicting"
    FINAL_BURN_INFLICTED = "burninflicted"
    ATTACK_HITS = "attackhits"


class EventData:
    def __init__(self, function: Callable[["EventData"], Any]=lambda ed: None, field=None, multiplier: float=None,
                 defender: "Pokemon"=None, attacker: "Pokemon"=None, damage=0, chance: float=None, crit_chance=None):
        """
        Function is a function which, when called, executes the event
        :param function:
        :param field:
        :param defender:
        :param attacker:
        :param damage:
        :param chance:
        """
        self.__multiplier = multiplier
        self.__field = field
        self.__defendant = defender
        self.__attacker = attacker
        self.__def_damage = damage
        self.__chance = chance
        self.__call = function
        self.__crit_chance = crit_chance

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

    @property
    def multiplier(self):
        return self.__multiplier

    @property
    def crit_chance(self):
        return self.__crit_chance


class Event:
    def __init__(self, event_type: EventType, data_object: EventData):
        self.__type = event_type
        self.__data = data_object

    def call(self):
        return self.__data.call()

    @property
    def type(self):
        return self.__type

