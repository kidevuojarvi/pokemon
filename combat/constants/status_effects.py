from Pokemon import Pokemon
from random import randint
from combat.event import Event, EventType


class StatusEffect:
    """
    Status effect on a pokemon. Has turn count and event emitter and handler
    """
    def __init__(self):
        self.__turns = 0

    def emit(self, affected: Pokemon) -> Event:
        raise NotImplementedError("Not implemented")

    def handle(self, event: Event):
        raise NotImplementedError("Not implemented")

    @property
    def turns(self):
        return self.__turns

    def increment_turns(self):
        self.__turns += 1


class SleepEffect(StatusEffect):
    def __init__(self, max_turns=randint(1, 3)):
        super().__init__()
        self.__max_turns = max_turns

    def handle(self, event: Event):
        if event.type() == EventType.POKEMON_ATTACKS:
            pass
            # TODO: Prevent pokemon from doing anything except sleep talk, switch etc.

    def emit(self, affected: Pokemon):
        # TODO: Actual event data implementation
        if self.turns > self.__max_turns:
            call = lambda: affected.remove_nonvol_status()
        else:
            call = lambda: None
        return Event(EventType.STATUS_REMOVED, call)


# Just for copying maths from
def burn_event(affected: Pokemon):
    """
    Affected pokemon loses 1/16 of it's max HP at the end of turn
    :param affected: Pokemon affected by burn
    :return: None
    """
    affected.damage(affected.get_max_hp() // 16)
    # TODO: Game prints information
    # TODO: Call for animation


def poison_event(affected: Pokemon):
    """
    Affected pokemon loses 1/8 of it's max HP at the end of turn
    :param affected: Pokemon affected by poison
    :return: None
    """
    affected.damage(affected.get_max_hp() // 8)
    # TODO: Game prints information
    # TODO: Call for animation


def toxic_event(affected: Pokemon):
    """
    Affected pokemon loses a cumulative 1/16 of it's max HP at the end of turn,
    then cumulative toxic count gets raised
    :param affected: Pokemon affected by toxic
    :return: None
    """
    toxic_count = affected.get_nonvol_status()[1]
    affected.damage(toxic_count * (affected.get_max_hp() // 16))
    affected.set_nonvol_status(("toxic", toxic_count + 1))

    # TODO: Game prints information
    # TODO: Call for animation


def leech_seed_event(affected: Pokemon, receiver: Pokemon):
    """
    Affected pokemon loses 1/8 of it's max HP, and the receiving pokemon gains
    an equal amount
    :param affected: Pokemon affected by Leech Seed
    :param receiver: Pokemon that gets healed
    :return: None
    """
    hp_lost = affected.damage(affected.get_max_hp() // 8)
    # TODO: Game prints information
    # TODO: Call for animation
    receiver.heal(hp_lost)
    # TODO: Game prints information


def flinch_event(affected: Pokemon):
    """
    Removes flinch from affected pokemon
    :param affected: Pokemon affected by flinch
    :return: None
    """
    affected.decrease_volatile_status_counter("flinch")


def curse_ghost_event(affected: Pokemon):
    """
    Deals damage to affected pokemon equal to 1/4 of it's max HP
    :param affected: Pokemon affected by curse
    :return: None
    """
    affected.damage(affected.get_max_hp() // 4)
    # TODO: Game prints information
    # TODO: Call for animation