import random

from typing import TYPE_CHECKING, List
from combat.event import Event, EventData, EventType
if TYPE_CHECKING:
    from combat.combat import Combat
    from combat.constants.status_effects import *


class MoveEffect:
    """
    The inflicted effect on the pokemon(s).
    Child classes create events which set the actual effects onto pokemons
    """
    def __init__(self, chance=None):
        self.__chance = chance

    @property
    def chance(self):
        return self.__chance

    def move_text(self):
        raise NotImplementedError("Not implemented")

    def affect(self, attacker: "Pokemon", defender: "Pokemon", world: "Combat") -> List["Event"]:
        raise NotImplementedError("Not implemented")


class MoveInflictSleep(MoveEffect):
    """
    Sleep status inflict
    """
    def __init__(self):
        super().__init__()

    def move_text(self):
        return "Puts the target to sleep"

    def affect(self, attacker: "Pokemon", defender: "Pokemon", world: "Combat") -> List["Event"]:
        def call(event_data: "EventData"):
            # Set the status
            if defender.no_nonvolatile_status():
                defender.set_nonvol_status(SleepEffect(defender))
            return []
        return [Event(EventType.STATUS_INFLICT_CHANCE, EventData(defender=defender, attacker=attacker,
                                                                 function=call))]

class MoveInflictParalyzeChance(MoveEffect):
    """
    Paralyze chance
    """
    def __init__(self, chance):
        super().__init__(chance)

    def move_text(self):
        # TODO: "How big a chance?"
        return "Has a chance to paralyze the target"

    def affect(self, attacker: "Pokemon", defender: "Pokemon", world: "Combat") -> List["Event"]:
        def call(event_data: "EventData"):
            # Set the status if rng
            r = random.randint(0, 100)
            if event_data.chance is None or r < event_data.chance:
                # TODO: The next check is wrong for some reason
                if defender.no_nonvolatile_status():
                    defender.set_nonvol_status(ParalyzeEffect(defender))
                    return [Event(EventType.STATUS_INFLICTED, EventData(lambda e: []))]
            return []
        return [Event(EventType.STATUS_INFLICT_CHANCE, EventData(chance=self.chance, defender=defender, attacker=attacker,
                                                                 function=call))]


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