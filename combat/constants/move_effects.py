from random import random

from combat.combat import Combat
from combat.constants.status_effects import *


class MoveEffect:
    """
    Instantiate this for a move.
    For example, a move has a chance to paralyze the target -> Make paralyze effect with a chance
    """
    def __init__(self, effect: MoveInflictEffect, chance: float=None):
        self.__chance = chance
        self.__effect = effect

    @property
    def chance(self):
        return self.__chance

    @chance.setter
    def chance(self, val):
        self.__chance = val

    @property
    def effect(self):
        return self.__effect

    def affect(self, attacker: Pokemon, defender: Pokemon, world: Combat):
        roll = random.random
        if self.chance is None or roll > self.chance:
            self.__effect.affect(attacker, defender, world)


class MoveInflictEffect:
    """
    The inflicted effect on the pokemon(s).
    Child classes are settable on Pokemon class as volatile or nonvolatile statuses.
    """
    def move_text(self):
        raise NotImplementedError("Not implemented")

    def affect(self, attacker: Pokemon, defender: Pokemon, world: Combat) -> Event:
        raise NotImplementedError("Not implemented")


class MoveInflictSleep(MoveInflictEffect):
    """
    Sleep status inflict
    """
    def __init__(self):
        super().__init__()

    def move_text(self):
        return "Puts the target to sleep"

    def affect(self, attacker: Pokemon, defender: Pokemon, world: Combat) -> Event:
        def call():
            if defender.no_nonvolatile_status():
                defender.set_nonvol_status(SleepEffect(defender))
        return Event(EventType.STATUS_INFLICTED, EventData(defendant=defender, attacker=attacker, function=call))

"""
def sleep_chance(attacker: Pokemon, defender: Pokemon, chance: int):
    if defender.get_nonvol_status() != None:
        return
    check = randint(0, 100)
    if check < chance:
        defender.set_nonvol_status(("sleep", 0))


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
"""