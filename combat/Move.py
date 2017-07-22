from typing import List, Callable
from Pokemon import Pokemon
from random import randint
from combat.constants.move_effects import MoveEffect

class Move:
    def __init__(self, name: str, power: int, accuracy: int, type: List[str],
                 category: str, contact: bool, effects: List[MoveEffect]):
        self.__name = name
        self.__power = power
        self.__accuracy = accuracy
        self.__type = type
        self.__category = category
        self.__contact = contact
        self.__effects = effects


    def get_name(self):
        return self.__name

    def get_power(self):
        return self.__power

    def get_accuracy(self):
        return self.__accuracy

    def get_type(self):
        return self.__type

    def get_category(self):
        return self.__category

    def get_contact(self):
        return self.__contact

    def get_effects(self):
        return self.__effects


