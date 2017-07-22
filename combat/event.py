from enum import Enum


class EventType(Enum):
    STATUS_AFFECTS_POKEMON = 0
    STATUS_INFLICTED = 1
    POKEMON_ATTACKS = 2
    STATUS_REMOVED = 3


class Event:
    # TODO: other event data
    def __init__(self, event_type: EventType, call):
        self.__type = event_type
        self.__call = call

    def type(self):
        return self.__type

    def call(self):
        self.__call()
