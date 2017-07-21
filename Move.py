from typing import List, Callable
from Pokemon import Pokemon
from random import randint

class Move:
    def __init__(self, name: str, power: int, accuracy: int, type: List[str],
                 category: str, contact: bool, effects: List[Callable]):
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


def burn_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "fire" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("burn", 0))


def poison_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "poison" in defender.get_types():
        return
    if "steel" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("poison", 0))


def toxic_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "poison" in defender.get_types():
        return
    if "steel" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("toxic", 1))


def paralysis_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "electric" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("para", 0))


def sleep_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("sleep", 0))


def freeze_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "ice" in defender.get_types():
        return
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("freeze", 0))


def flinch_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "flinch" in defender.get_volatile_statuses():
        return
    check = randint(0, 100)
    if check < chance:
        defender.add_volatile_status("flinch")


def confusion_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if "confusion" in defender.get_volatile_statuses():
        return
    check = randint(0, 100)
    if check < chance:
        defender.add_volatile_status("confusion")


def curse_ghost(attacker: Pokemon, defender: Pokemon):
    if "curse" in defender.get_volatile_statuses():
        return
    defender.add_volatile_status("curse")


def leech_seed(attacker: Pokemon, defender: Pokemon):
    if "grass" in defender.get_types():
        return
    if "leech_seed" in defender.get_volatile_statuses():
        return
    defender.add_volatile_status("leech_seed")