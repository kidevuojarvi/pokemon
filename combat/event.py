from enum import Enum, auto
from typing import Callable, List, TYPE_CHECKING, Any
import random

if TYPE_CHECKING:
    from Pokemon import Pokemon
    from combat.Move import Move


class EventType(Enum):
    SLEEP_INFLICTING = auto()
    FINAL_SLEEP_INFLICTED = auto()
    PARALYZE_INFLICTING = auto()
    FINAL_PARALYZE_INFLICTED = auto()
    ATTACK_TRIES_TO_HIT = auto()
    FINAL_ATTACK_DID_DAMAGE = auto()
    FINAL_ATTACK_CRIT = auto()
    RECOIL_DAMAGE = auto()
    FINAL_TOOK_RECOIL_DAMAGE = auto()
    ABSORB_HEALTH = auto()
    FINAL_HEALTH_ABSORBED = auto()
    STATUS_REMOVE = auto()
    TURN_END = auto()
    FINAL_ATTACK_MISSES = auto()
    ATTACK_DOES_EXACT_DAMAGE = auto()
    ATTACK_FAILED = auto()
    MULTI_HIT_TIMES = auto()
    BURN_INFLICTING = auto()
    FINAL_BURN_INFLICTED = auto()
    ATTACK_HITS = auto()


class EventData:
    def __init__(self, function: Callable[["EventData"], Any]=lambda ed: None, field=None, multiplier: float=None,
                 defender: "Pokemon"=None, attacker: "Pokemon"=None, damage=0, chance: float=None, crit_chance=None,
                 move: "Move"=None):
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
        self.__move = move

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

    @property
    def move(self):
        return self.__move


class Event:
    def __init__(self, event_type: EventType, data_object: EventData):
        self.__type = event_type
        self.__data = data_object

    def call(self):
        return self.__data.call()

    @property
    def type(self):
        return self.__type

